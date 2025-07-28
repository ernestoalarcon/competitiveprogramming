// src/models/DataStore.ts

import { ApolloClient, ObservableQuery } from "@apollo/client";
import { GET_DATA_SUBSCRIPTION } from "./graphql"; // Asume que tienes tu suscripción GraphQL aquí

// Interfaz para nuestros datos de fila.
// - _isDirty: El usuario ha modificado esta fila localmente.
// - _isStale: El servidor tiene una versión más nueva que la que el usuario está editando.
export interface IRowData {
  id: string; // Un ID único es crucial
  // ...otros campos de datos (ej: a, b, c)
  [key: string]: any;
  _isDirty?: boolean;
  _isStale?: boolean;
}

// Un helper para "ceder" (yield) datos a nuestro generador asíncrono.
class YieldController<T> {
  private _resolve: ((value: T) => void) | null = null;

  yield(value: T) {
    if (this._resolve) {
      this._resolve(value);
      this._resolve = null;
    }
  }

  waitForNextYield(): Promise<T> {
    return new Promise((resolve) => {
      this._resolve = resolve;
    });
  }
}

export class DataStore {
  // 1. ESTADO INTERNO
  // Usamos un Map para acceso O(1) por ID, mucho más rápido que find() en un array.
  private data = new Map<string, IRowData>();
  private incomingUpdatesQueue: IRowData[] = [];
  private batchTimeout: NodeJS.Timeout | null = null;
  private isProcessing = false;

  // 2. CONEXIÓN CON REACT (Async Generator)
  private yieldController = new YieldController<IRowData[]>();

  public async *getUpdates(): AsyncGenerator<IRowData[]> {
    // Cede el estado inicial inmediatamente
    yield Array.from(this.data.values());

    while (true) {
      const newDataSet = await this.yieldController.waitForNextYield();
      yield newDataSet;
    }
  }

  // 3. LÓGICA DE SUSCRIPCIÓN Y BATCHING
  public startSubscription(client: ApolloClient<any>) {
    // Aquí es donde te suscribes a GraphQL
    const observable = client.subscribe({ query: GET_DATA_SUBSCRIPTION });

    observable.subscribe({
      next: (response) => {
        // En lugar de actualizar la UI, encolamos el dato y planificamos el procesamiento
        const newData = response.data.yourSubscriptionName as IRowData;
        this.incomingUpdatesQueue.push(newData);
        this.scheduleBatchProcessing();
      },
      error: (err) => console.error("Subscription error", err),
    });
  }

  private scheduleBatchProcessing() {
    // Si ya hay un lote planificado o se está procesando uno, no hagas nada.
    if (this.batchTimeout || this.isProcessing) {
      return;
    }

    // Planifica el procesamiento en 300ms.
    this.batchTimeout = setTimeout(() => {
      this.processBatch();
      this.batchTimeout = null;
    }, 300);
  }

  // 4. LÓGICA DE FUSIÓN (EL CORAZÓN DE LA SOLUCIÓN)
  private processBatch() {
    if (this.isProcessing) return;
    this.isProcessing = true;

    const updatesToProcess = [...this.incomingUpdatesQueue];
    this.incomingUpdatesQueue = [];

    let hasChanges = false;

    for (const update of updatesToProcess) {
      const existingRow = this.data.get(update.id);

      // CASO 1: La fila ya está siendo editada por el usuario ("dirty").
      if (existingRow?._isDirty) {
        // No sobrescribimos los datos del usuario.
        // En su lugar, marcamos la fila como "desactualizada" para notificarle.
        if (!existingRow._isStale) {
          existingRow._isStale = true;
          hasChanges = true;
        }
        continue; // Saltar a la siguiente actualización
      }

      // CASO 2: La fila no está siendo editada, la actualizamos de forma segura.
      this.data.set(update.id, { ...update, _isDirty: false, _isStale: false });
      hasChanges = true;
    }

    if (hasChanges) {
      this.yieldToConsumer();
    }

    this.isProcessing = false;

    // Si llegaron más datos mientras procesábamos, planifica otro lote.
    if (this.incomingUpdatesQueue.length > 0) {
      this.scheduleBatchProcessing();
    }
  }

  // 5. MANEJO DE EDICIONES DEL USUARIO
  public handleUserEdit(id: string, field: string, value: any) {
    const row = this.data.get(id);
    if (row) {
      const updatedRow = {
        ...row,
        [field]: value,
        _isDirty: true, // ¡Marcamos la fila como "sucia"!
      };
      this.data.set(id, updatedRow);
      // Cedemos el cambio del usuario inmediatamente para que la UI sea responsiva.
      this.yieldToConsumer();
    }
  }

  private yieldToConsumer() {
    // Cede una nueva copia del array para que React detecte el cambio.
    this.yieldController.yield(Array.from(this.data.values()));
  }
}
