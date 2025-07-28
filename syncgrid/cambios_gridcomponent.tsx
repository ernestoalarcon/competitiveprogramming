// src/components/GridComponent.tsx (MEJORADO)

import React, {
  useState,
  useEffect,
  useMemo,
  useRef,
  useCallback,
} from "react";
import { AgGridReact } from "ag-grid-react";
import {
  ColDef,
  GridApi,
  GridReadyEvent,
  GetRowIdParams,
  ValueSetterParams,
} from "ag-grid-community";
import { useApolloClient } from "@apollo/client";

import "ag-grid-community/styles/ag-grid.css";
import "ag-grid-community/styles/ag-theme-alpine.css";
import "./GridStyles.css";

import { DataStore, IRowData } from "../models/DataStore";

export const GridComponent: React.FC = () => {
  const apolloClient = useApolloClient();
  const [dataStore] = useState(() => new DataStore());

  // CAMBIO CLAVE: El estado de rowData solo se usa para la carga INICIAL.
  const [rowData, setRowData] = useState<IRowData[]>([]);

  // La referencia a la API del grid es ahora más importante que nunca.
  const gridApiRef = useRef<GridApi<IRowData>>();

  useEffect(() => {
    let isMounted = true;

    // Cargamos los datos iniciales una sola vez.
    setRowData(dataStore.getInitialData());

    dataStore.startSubscription(apolloClient);

    const consumeUpdates = async () => {
      // Esperamos a que el grid esté listo antes de procesar transacciones.
      if (!gridApiRef.current) {
        // Podríamos usar un event listener o un simple timeout para reintentar.
        setTimeout(consumeUpdates, 100);
        return;
      }

      for await (const transaction of dataStore.getUpdates()) {
        if (isMounted && gridApiRef.current) {
          // CAMBIO CLAVE: Usamos applyTransactionAsync para la máxima eficiencia.
          // Esta API no bloquea el hilo principal y procesa la transacción en segundo plano.
          gridApiRef.current.applyTransactionAsync(transaction);
        }
      }
    };

    consumeUpdates();

    return () => {
      isMounted = false;
    };
  }, [dataStore, apolloClient]);

  // La función onGridReady es crucial para capturar la API.
  const onGridReady = useCallback((params: GridReadyEvent<IRowData>) => {
    gridApiRef.current = params.api;
  }, []);

  // El resto del componente (colDefs, onCellValueChanged, getRowId) es prácticamente igual.
  const colDefs = useMemo<ColDef[]>(
    [
      // ... (sin cambios)
    ],
    []
  );

  const onCellValueChanged = (params: ValueSetterParams) => {
    // ... (sin cambios, sigue llamando a dataStore.handleUserEdit)
  };

  const getRowId = (params: GetRowIdParams) => params.data.id;

  return (
    <div className="ag-theme-alpine" style={{ height: "600px", width: "100%" }}>
      <AgGridReact
        rowData={rowData} // Solo para la carga inicial
        columnDefs={colDefs}
        getRowId={getRowId}
        onGridReady={onGridReady}
        onCellValueChanged={onCellValueChanged}
        // Ya no necesitamos asyncTransactionWaitMillis aquí, porque nuestro DataStore
        // ya se encarga del batching de una forma más controlada.
      />
    </div>
  );
};
