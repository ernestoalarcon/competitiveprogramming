// src/components/GridComponent.tsx

import React, { useState, useEffect, useMemo } from "react";
import { AgGridReact } from "ag-grid-react";
import { ColDef, ValueSetterParams, GetRowIdParams } from "ag-grid-community";
import { useApolloClient } from "@apollo/client";

import "ag-grid-community/styles/ag-grid.css";
import "ag-grid-community/styles/ag-theme-alpine.css";
import "./GridStyles.css"; // Estilos para las filas desactualizadas

import { DataStore, IRowData } from "../models/DataStore";

export const GridComponent: React.FC = () => {
  // El cliente Apollo para pasarlo al store
  const apolloClient = useApolloClient();

  // Instanciamos nuestro DataStore. Usamos useState con una función para que solo se cree una vez.
  const [dataStore] = useState(() => new DataStore());

  // El estado que alimentará a AgGrid
  const [rowData, setRowData] = useState<IRowData[]>([]);

  // useEffect para conectar el componente al DataStore.
  useEffect(() => {
    let isMounted = true;

    // Iniciamos la suscripción GraphQL dentro del store
    dataStore.startSubscription(apolloClient);

    // Creamos una función asíncrona para consumir el generador
    const consumeUpdates = async () => {
      for await (const data of dataStore.getUpdates()) {
        if (isMounted) {
          // Cada vez que el store "ceda" nuevos datos, actualizamos el estado de React.
          setRowData(data);
        }
      }
    };

    consumeUpdates();

    return () => {
      isMounted = false;
      // Aquí podrías agregar lógica para detener la suscripción si es necesario
    };
  }, [dataStore, apolloClient]); // Se ejecuta solo una vez

  // Definiciones de columnas para AgGrid
  const colDefs = useMemo<ColDef[]>(
    () => [
      { field: "id", editable: false, headerName: "ID" },
      { field: "a", editable: true },
      { field: "b", editable: true },
      // ...otras columnas
      {
        headerName: "Estado",
        width: 100,
        editable: false,
        // Usamos `valueGetter` para mostrar un estado basado en nuestras flags internas.
        valueGetter: (params) => {
          if (params.data?._isStale) return "⚠️ Desactualizado";
          if (params.data?._isDirty) return "✎ Editando...";
          return "Sincronizado";
        },
        // Cambiamos el estilo de la celda si está desactualizada.
        cellClassRules: {
          "cell-stale": (params) => params.data?._isStale === true,
          "cell-dirty": (params) => params.data?._isDirty === true,
        },
      },
    ],
    []
  );

  // Callback para cuando el usuario edita una celda en el grid
  const onCellValueChanged = (params: ValueSetterParams) => {
    const { data, colDef, newValue } = params;
    // Informamos al DataStore sobre la edición
    dataStore.handleUserEdit(data.id, colDef.field!, newValue);
  };

  // MUY IMPORTANTE: Esta función le dice a AgGrid cómo identificar cada fila de forma única.
  // Esto permite a AgGrid realizar actualizaciones de transacciones eficientes en lugar de volver a renderizar todo.
  const getRowId = (params: GetRowIdParams) => params.data.id;

  return (
    <div className="ag-theme-alpine" style={{ height: "600px", width: "100%" }}>
      <AgGridReact
        rowData={rowData}
        columnDefs={colDefs}
        getRowId={getRowId}
        onCellValueChanged={onCellValueChanged}
        // Habilitamos las transacciones asíncronas para el mejor rendimiento
        asyncTransactionWaitMillis={500}
      />
    </div>
  );
};
