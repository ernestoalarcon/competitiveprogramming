Claro, aquí tienes una implementación profesional de una clase `FDC3Model` en TypeScript que encapsula toda la lógica de FDC3, junto con ejemplos de cómo integrarla en una aplicación React de manera limpia y eficiente.

---

### `FDC3Model`: La Capa de Abstracción para FDC3

Esta clase singleton se encarga de toda la comunicación con la API de FDC3. Los componentes de React no interactuarán directamente con `window.fdc3`, sino a través de esta capa de servicio, promoviendo una clara separación de responsabilidades.

#### **`src/fdc3/FDC3Model.ts`**

```typescript
import {
  DesktopAgent,
  Channel,
  Context,
  Listener,
  AppIntent,
  IntentResolution,
  ContextHandler,
  PrivateChannel,
} from "@finos/fdc3";

/**
 * FDC3Model es una clase singleton que encapsula todas las interacciones
 * con la API de FDC3, proveyendo una capa de abstracción para la UI.
 */
export class FDC3Model {
  private static instance: FDC3Model;
  private fdc3: DesktopAgent | null = null;
  private ready: Promise<void>;

  private constructor() {
    // El 'resolver' de la promesa se almacena para llamarlo cuando fdc3 esté listo.
    let resolveReady: () => void;
    this.ready = new Promise<void>((resolve) => {
      resolveReady = resolve;
    });

    this.initializeFDC3(resolveReady!);
  }

  private async initializeFDC3(resolveReady: () => void): Promise<void> {
    try {
      // Espera a que el agente FDC3 esté disponible en el objeto window.
      this.fdc3 = await (window as any).fdc3;
      if (this.fdc3) {
        console.log("FDC3 Agent está listo.");
        resolveReady();
      } else {
        throw new Error("El agente FDC3 no se encontró en window.fdc3.");
      }
    } catch (error) {
      console.error("Error al inicializar FDC3:", error);
      // En un escenario real, podrías querer manejar este error de forma más robusta.
    }
  }

  /**
   * Obtiene la instancia singleton de FDC3Model.
   */
  public static getInstance(): FDC3Model {
    if (!FDC3Model.instance) {
      FDC3Model.instance = new FDC3Model();
    }
    return FDC3Model.instance;
  }

  /**
   * Asegura que el agente FDC3 esté listo antes de ejecutar cualquier operación.
   */
  private async ensureReady(): Promise<DesktopAgent> {
    await this.ready;
    if (!this.fdc3) {
      throw new Error("FDC3 no está inicializado.");
    }
    return this.fdc3;
  }

  // MÉTODOS DE CONTEXTO
  // ------------------

  /**
   * Difunde un contexto a todas las aplicaciones en el escritorio.
   * @param context El contexto a difundir.
   */
  public async broadcast<T extends Context>(context: T): Promise<void> {
    const fdc3 = await this.ensureReady();
    await fdc3.broadcast(context);
    console.log("Contexto difundido:", context);
  }

  /**
   * Añade un listener para un tipo de contexto específico.
   * @param contextType El tipo de contexto a escuchar (e.g., 'fdc3.instrument').
   * @param handler La función que manejará el contexto recibido.
   * @returns Una promesa que resuelve a un objeto Listener para poder desuscribirse.
   */
  public async addContextListener<T extends Context>(
    contextType: string | null,
    handler: ContextHandler<T>
  ): Promise<Listener> {
    const fdc3 = await this.ensureReady();
    return fdc3.addContextListener(
      contextType,
      handler as ContextHandler<Context>
    );
  }

  // MÉTODOS DE INTENTS
  // -------------------

  /**
   * Lanza un intent para que otra aplicación lo maneje.
   * @param intent El nombre del intent (e.g., 'ViewChart').
   * @param context El contexto asociado al intent.
   * @returns Una promesa que resuelve a la resolución del intent.
   */
  public async raiseIntent<T extends Context>(
    intent: string,
    context: T
  ): Promise<IntentResolution> {
    const fdc3 = await this.ensureReady();
    return fdc3.raiseIntent(intent, context);
  }

  /**
   * Registra un listener para un intent específico.
   * @param intent El nombre del intent a escuchar.
   * @param handler El manejador para cuando se reciba el intent.
   * @returns Una promesa que resuelve a un objeto Listener.
   */
  public async addIntentListener<T extends Context>(
    intent: string,
    handler: ContextHandler<T>
  ): Promise<Listener> {
    const fdc3 = await this.ensureReady();
    return fdc3.addIntentListener(intent, handler as ContextHandler<Context>);
  }

  // MÉTODOS DE CANALES
  // -----------------

  /**
   * Obtiene la lista de canales de usuario disponibles.
   */
  public async getUserChannels(): Promise<Channel[]> {
    const fdc3 = await this.ensureReady();
    return fdc3.getUserChannels();
  }

  /**
   * Une la aplicación a un canal de usuario específico por su ID.
   * @param channelId El ID del canal al que unirse.
   */
  public async joinUserChannel(channelId: string): Promise<void> {
    const fdc3 = await this.ensureReady();
    await fdc3.joinUserChannel(channelId);
    console.log(`Unido al canal: ${channelId}`);
  }

  /**
   * Obtiene el canal actual al que está unida la aplicación.
   */
  public async getCurrentChannel(): Promise<Channel | null> {
    const fdc3 = await this.ensureReady();
    return fdc3.getCurrentChannel();
  }

  /**
   * Abandona el canal actual.
   */
  public async leaveCurrentChannel(): Promise<void> {
    const fdc3 = await this.ensureReady();
    await fdc3.leaveCurrentChannel();
    console.log("Se ha abandonado el canal actual.");
  }

  /**
   * Crea un canal privado para comunicación punto a punto.
   * Ideal para devolver como resultado de un intent.
   */
  public async createPrivateChannel(): Promise<PrivateChannel> {
    const fdc3 = await this.ensureReady();
    return fdc3.createPrivateChannel();
  }
}
```

---

### Integración con React

Para usar `FDC3Model` en React, crearemos un hook simple y luego lo consumiremos desde nuestros componentes.

#### **`src/hooks/useFDC3.ts`**

Este hook simplemente proporciona la instancia del modelo a los componentes.

```typescript
import { FDC3Model } from "../fdc3/FDC3Model";

/**
 * Hook de React para acceder a la instancia singleton de FDC3Model.
 */
export const useFDC3 = (): FDC3Model => {
  return FDC3Model.getInstance();
};
```

#### **Ejemplos de Componentes React**

Aquí mostramos cómo diferentes componentes pueden usar el hook `useFDC3` para interactuar con el escritorio sin conocer los detalles de la API de FDC3.

**1. Componente para Difundir un Contexto** BROADCASTER

Este componente difunde un contexto de instrumento (`fdc3.instrument`) o un contexto personalizado (`myorg.order`).

```typescript
// src/components/Broadcaster.tsx
import React from "react";
import { useFDC3 } from "../hooks/useFDC3";
import { Instrument } from "@finos/fdc3";

// Definimos un tipo para nuestro contexto personalizado
interface MyOrderContext extends Context {
  type: "myorg.order";
  orderId: string;
  quantity: number;
}

const Broadcaster: React.FC = () => {
  const fdc3 = useFDC3();

  const handleBroadcastInstrument = () => {
    const instrument: Instrument = {
      type: "fdc3.instrument",
      id: { ticker: "MSFT" },
      name: "Microsoft Corp",
    };
    fdc3.broadcast(instrument).catch(console.error);
  };

  const handleBroadcastCustom = () => {
    const order: MyOrderContext = {
      type: "myorg.order",
      orderId: `ord-${Date.now()}`,
      quantity: 500,
    };
    fdc3.broadcast(order).catch(console.error);
  };

  return (
    <div style={{ border: "1px solid #ccc", padding: "10px", margin: "10px" }}>
      <h4>📣 Broadcaster</h4>
      <button onClick={handleBroadcastInstrument}>
        Broadcast Instrument (MSFT)
      </button>
      <button onClick={handleBroadcastCustom}>Broadcast Custom Order</button>
    </div>
  );
};

export default Broadcaster;
```

**2. Componente para Escuchar Contextos** 👂

Este componente escucha cualquier contexto y lo muestra en la UI.

```typescript
// src/components/ContextLogger.tsx
import React, { useState, useEffect } from "react";
import { useFDC3 } from "../hooks/useFDC3";
import { Context, Listener } from "@finos/fdc3";

const ContextLogger: React.FC = () => {
  const fdc3 = useFDC3();
  const [lastContext, setLastContext] = useState<Context | null>(null);

  useEffect(() => {
    let listener: Listener;

    const setupListener = async () => {
      // Escuchamos CUALQUIER contexto (pasando null como tipo)
      listener = await fdc3.addContextListener(null, (context) => {
        console.log("Contexto recibido:", context);
        setLastContext(context);
      });
    };

    setupListener().catch(console.error);

    // Función de limpieza para desuscribirse
    return () => {
      if (listener) {
        listener.unsubscribe();
      }
    };
  }, [fdc3]); // El efecto se ejecuta solo una vez

  return (
    <div style={{ border: "1px solid #ccc", padding: "10px", margin: "10px" }}>
      <h4>👂 Context Logger</h4>
      <p>Último contexto recibido:</p>
      <pre>
        {JSON.stringify(lastContext, null, 2) || "Esperando contexto..."}
      </pre>
    </div>
  );
};

export default ContextLogger;
```

**3. Componente para Manejar Canales e Intents** 🚀

Este componente permite unirse a un canal de usuario y lanzar un intent `ViewChart`.

```typescript
// src/components/ActionsController.tsx
import React, { useState, useEffect } from "react";
import { useFDC3 } from "../hooks/useFDC3";
import { Channel, Instrument } from "@finos/fdc3";

const ActionsController: React.FC = () => {
  const fdc3 = useFDC3();
  const [channels, setChannels] = useState<Channel[]>([]);
  const [currentChannel, setCurrentChannel] = useState<Channel | null>(null);

  useEffect(() => {
    fdc3.getUserChannels().then(setChannels).catch(console.error);
  }, [fdc3]);

  const handleJoinChannel = async (id: string) => {
    await fdc3.joinUserChannel(id);
    const channel = await fdc3.getCurrentChannel();
    setCurrentChannel(channel);
  };

  const handleLeaveChannel = async () => {
    await fdc3.leaveCurrentChannel();
    setCurrentChannel(null);
  };

  const handleRaiseIntent = () => {
    const instrument: Instrument = {
      type: "fdc3.instrument",
      id: { ticker: "GOOGL" },
    };
    fdc3
      .raiseIntent("ViewChart", instrument)
      .then((resolution) => console.log("Intent resuelto:", resolution))
      .catch((error) => console.error("Fallo al lanzar intent:", error));
  };

  return (
    <div style={{ border: "1px solid #ccc", padding: "10px", margin: "10px" }}>
      <h4>🚀 Actions Controller</h4>
      <div>
        <strong>Canales:</strong>
        {channels.map((c) => (
          <button key={c.id} onClick={() => handleJoinChannel(c.id)}>
            Unirse a {c.id}
          </button>
        ))}
        <button onClick={handleLeaveChannel} disabled={!currentChannel}>
          Salir del canal
        </button>
        {currentChannel && <p>Canal actual: {currentChannel.id}</p>}
      </div>
      <hr />
      <div>
        <strong>Intents:</strong>
        <button onClick={handleRaiseIntent}>
          Lanzar Intent "ViewChart" (GOOGL)
        </button>
      </div>
    </div>
  );
};

export default ActionsController;
```

Con esta estructura, has creado un sistema robusto y escalable. La clase `FDC3Model` maneja toda la complejidad de la API, y tus componentes React se mantienen limpios, declarativos y fáciles de probar, consumiendo la lógica de FDC3 a través de un hook simple y claro.
