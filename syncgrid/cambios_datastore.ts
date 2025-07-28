// src/models/DataStore.ts (MEJORADO)

// ... (las interfaces IRowData y YieldController no cambian)

// CAMBIO CLAVE: Definimos un tipo para nuestras transacciones.
export interface ITransaction {
  add: IRowData[];
  update: IRowData[];
  remove: IRowData[];
}

export class DataStore {
  private data = new Map<string, IRowData>();
  private incomingUpdatesQueue: IRowData[] = [];
  private batchTimeout: NodeJS.Timeout | null = null;
  private isProcessing = false;

  // CAMBIO CLAVE: El generador ahora cede objetos de transacción.
  private yieldController = new YieldController<ITransaction>();

  public async *getUpdates(): AsyncGenerator<ITransaction> {
    while (true) {
      const transaction = await this.yieldController.waitForNextYield();
      yield transaction;
    }
  }

  // Obtenemos los datos iniciales para la primera carga del grid.
  public getInitialData(): IRowData[] {
    // Aquí podrías tener una lógica para cargar un snapshot inicial si es necesario.
    return Array.from(this.data.values());
  }

  // ... (startSubscription y scheduleBatchProcessing no cambian)

  private processBatch() {
    if (this.isProcessing) return;
    this.isProcessing = true;

    const updatesToProcess = [...this.incomingUpdatesQueue];
    this.incomingUpdatesQueue = [];

    // CAMBIO CLAVE: Construimos el objeto de transacción.
    const transaction: ITransaction = { add: [], update: [], remove: [] };

    for (const update of updatesToProcess) {
      const existingRow = this.data.get(update.id);

      if (existingRow?._isDirty) {
        if (!existingRow._isStale) {
          existingRow._isStale = true;
          // Aunque está "sucia", sigue siendo una actualización para la transacción.
          transaction.update.push(existingRow);
        }
        continue;
      }

      // Si la fila ya existe, es una actualización. Si no, es una adición.
      if (existingRow) {
        transaction.update.push(update);
      } else {
        transaction.add.push(update);
      }

      // Actualizamos nuestro estado interno.
      this.data.set(update.id, { ...update, _isDirty: false, _isStale: false });
    }

    if (transaction.add.length > 0 || transaction.update.length > 0) {
      this.yieldToConsumer(transaction);
    }

    this.isProcessing = false;

    if (this.incomingUpdatesQueue.length > 0) {
      this.scheduleBatchProcessing();
    }
  }

  public handleUserEdit(id: string, field: string, value: any) {
    const row = this.data.get(id);
    if (row) {
      const updatedRow = { ...row, [field]: value, _isDirty: true };
      this.data.set(id, updatedRow);

      // CAMBIO CLAVE: Cedemos una transacción solo con la fila actualizada.
      this.yieldToConsumer({
        add: [],
        update: [updatedRow],
        remove: [],
      });
    }
  }

  private yieldToConsumer(transaction: ITransaction) {
    this.yieldController.yield(transaction);
  }
}
