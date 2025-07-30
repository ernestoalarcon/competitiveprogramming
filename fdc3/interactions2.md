## Dominando FDC3 con TypeScript y React: Una Guía Detallada

El estándar **Financial Desktop Connectivity and Collaboration Consortium (FDC3)** está revolucionando la forma en que las aplicaciones financieras interactúan en el escritorio. Al proporcionar un conjunto de API estandarizadas, FDC3 permite una interoperabilidad fluida, eliminando los silos de información y mejorando la eficiencia del flujo de trabajo. Esta guía te enseñará detalladamente a utilizar la API de FDC3 con **TypeScript** y **React**, proporcionando ejemplos de calidad profesional para que puedas construir aplicaciones financieras conectadas y robustas.

### Configuración del Entorno con React y TypeScript

Para comenzar, es fundamental tener un entorno de desarrollo que soporte FDC3. La mayoría de los contenedores de escritorio modernos (como OpenFin, Finsemble o Glue42) proporcionan una implementación de la API FDC3. Para nuestras aplicaciones React, utilizaremos el paquete `@finos/fdc3` para obtener las definiciones de tipo de TypeScript.

Primero, inicializa un proyecto de React con TypeScript:

```bash
npx create-react-app mi-app-fdc3 --template typescript
cd mi-app-fdc3
```

Luego, instala el paquete FDC3:

```bash
npm install @finos/fdc3
```

Ahora, puedes acceder a la API de FDC3 a través del objeto `window.fdc3`. Es una buena práctica crear un hook de React para gestionar la disponibilidad de la API:

```typescript
// src/hooks/useFdc3.ts
import { useEffect, useState } from "react";
import { DesktopAgent } from "@finos/fdc3";

export const useFdc3 = () => {
  const [fdc3, setFdc3] = useState<DesktopAgent | null>(null);

  useEffect(() => {
    const getFdc3 = async () => {
      try {
        const agent = await (window as any).fdc3;
        setFdc3(agent);
      } catch (error) {
        console.error("FDC3 no está disponible.", error);
      }
    };

    getFdc3();
  }, []);

  return fdc3;
};
```

---

### Contextos de Datos (Data Contexts): El Lenguaje Común

Los contextos de datos son el pilar de la comunicación en FDC3. Son objetos JSON con una estructura predefinida que representan entidades del mundo real como instrumentos financieros, contactos u organizaciones.

#### Contextos Estándar

FDC3 define una serie de contextos estándar que cubren los casos de uso más comunes. Por ejemplo, el contexto `fdc3.instrument` representa un instrumento financiero.

**Ejemplo: Creación y difusión de un contexto de instrumento**

```typescript
// src/components/InstrumentPanel.tsx
import React from "react";
import { Instrument } from "@finos/fdc3";
import { useFdc3 } from "../hooks/useFdc3";

const InstrumentPanel: React.FC = () => {
  const fdc3 = useFdc3();

  const broadcastInstrument = async () => {
    if (fdc3) {
      const instrumentContext: Instrument = {
        type: "fdc3.instrument",
        id: {
          ticker: "AAPL",
        },
        name: "Apple Inc.",
      };

      try {
        await fdc3.broadcast(instrumentContext);
        console.log("Contexto de instrumento difundido:", instrumentContext);
      } catch (error) {
        console.error("Error al difundir el contexto:", error);
      }
    }
  };

  return (
    <div>
      <h2>Panel de Instrumentos</h2>
      <button onClick={broadcastInstrument}>Difundir Apple (AAPL)</button>
    </div>
  );
};

export default InstrumentPanel;
```

#### Contextos Personalizados (Custom Contexts)

Cuando los contextos estándar no son suficientes, puedes definir tus propios contextos. La única regla es que el tipo (`type`) no debe comenzar con `fdc3.`. Es una buena práctica utilizar un prefijo de tu organización (ej. `myorg.mycontext`).

**Ejemplo: Definición y uso de un contexto de orden personalizado**

```typescript
// src/types/customContexts.ts
import { Context } from "@finos/fdc3";

export interface MyOrderContext extends Context {
  type: "myorg.order";
  orderId: string;
  quantity: number;
  side: "buy" | "sell";
}
```

```typescript
// src/components/OrderTicket.tsx
import React from "react";
import { useFdc3 } from "../hooks/useFdc3";
import { MyOrderContext } from "../types/customContexts";
import { Instrument } from "@finos/fdc3";

const OrderTicket: React.FC = () => {
  const fdc3 = useFdc3();
  const [instrument, setInstrument] = React.useState<Instrument | null>(null);

  React.useEffect(() => {
    if (fdc3) {
      const listener = fdc3.addContextListener("fdc3.instrument", (context) => {
        setInstrument(context as Instrument);
      });
      return () => listener.unsubscribe();
    }
  }, [fdc3]);

  const placeOrder = async () => {
    if (fdc3 && instrument) {
      const orderContext: MyOrderContext = {
        type: "myorg.order",
        orderId: `ORD-${Date.now()}`,
        quantity: 100,
        side: "buy",
        name: `Buy 100 ${instrument.id?.ticker}`,
      };

      try {
        await fdc3.broadcast(orderContext);
        console.log("Orden personalizada difundida:", orderContext);
      } catch (error) {
        console.error("Error al difundir la orden:", error);
      }
    }
  };

  return (
    <div>
      <h2>Boleta de Órdenes</h2>
      {instrument ? (
        <>
          <p>
            Instrumento: {instrument.name} ({instrument.id?.ticker})
          </p>
          <button onClick={placeOrder}>Colocar Orden de Compra</button>
        </>
      ) : (
        <p>Esperando contexto de instrumento...</p>
      )}
    </div>
  );
};

export default OrderTicket;
```

---

### Intents: Acciones con Propósito

Los **Intents** son verbos que describen una acción que un usuario desea realizar, como `ViewChart` o `StartChat`. Las aplicaciones pueden registrarse para manejar intents específicos para ciertos tipos de contexto.

**Ejemplo: Lanzar un intent `ViewChart`**

```typescript
// src/components/InstrumentDetails.tsx
import React from "react";
import { useFdc3 } from "../hooks/useFdc3";
import { Instrument } from "@finos/fdc3";

const InstrumentDetails: React.FC = () => {
  const fdc3 = useFdc3();

  const viewChart = async () => {
    if (fdc3) {
      const instrumentContext: Instrument = {
        type: "fdc3.instrument",
        id: {
          ticker: "GOOGL",
        },
      };
      try {
        await fdc3.raiseIntent("ViewChart", instrumentContext);
      } catch (error) {
        console.error("Error al lanzar el intent ViewChart:", error);
      }
    }
  };

  return (
    <div>
      <button onClick={viewChart}>Ver Gráfico de Google</button>
    </div>
  );
};

export default InstrumentDetails;
```

**Ejemplo: Registrar un listener para un intent**

Una aplicación de gráficos se registraría de la siguiente manera para manejar el intent `ViewChart`:

```typescript
// En la aplicación de gráficos
import { useFdc3 } from "../hooks/useFdc3";
import React, { useEffect, useState } from "react";
import { Instrument } from "@finos/fdc3";

const ChartComponent: React.FC = () => {
  const fdc3 = useFdc3();
  const [instrument, setInstrument] = useState<Instrument | null>(null);

  useEffect(() => {
    if (fdc3) {
      const listener = fdc3.addIntentListener("ViewChart", (context) => {
        // Lógica para mostrar el gráfico para el instrumento recibido
        setInstrument(context as Instrument);
        console.log("Manejando intent ViewChart para:", context);
      });
      return () => listener.unsubscribe();
    }
  }, [fdc3]);

  return (
    <div>
      {instrument
        ? `Mostrando gráfico para ${instrument.id?.ticker}`
        : "Esperando un instrumento..."}
    </div>
  );
};
```

---

### Canales (Channels): Comunicación Contextual

Los canales permiten una comunicación más acotada que la difusión global. Las aplicaciones pueden unirse a canales (ya sean de usuario o de aplicación) para compartir contexto solo con otras aplicaciones en el mismo canal.

#### Canales de Usuario (User Channels)

Son canales predefinidos por el contenedor de escritorio, a menudo representados por colores (rojo, verde, azul, etc.).

**Ejemplo: Unirse a un canal y escuchar contexto**

```typescript
// src/components/ChannelSelector.tsx
import React, { useEffect, useState } from "react";
import { useFdc3 } from "../hooks/useFdc3";
import { Channel, DisplayMetadata, Instrument } from "@finos/fdc3";

const ChannelSelector: React.FC = () => {
  const fdc3 = useFdc3();
  const [channels, setChannels] = useState<
    (Channel & { displayMetadata: DisplayMetadata })[]
  >([]);
  const [currentInstrument, setCurrentInstrument] = useState<Instrument | null>(
    null
  );

  useEffect(() => {
    const fetchChannels = async () => {
      if (fdc3) {
        const userChannels = await fdc3.getUserChannels();
        setChannels(userChannels);
      }
    };
    fetchChannels();
  }, [fdc3]);

  const joinChannel = async (channelId: string) => {
    if (fdc3) {
      await fdc3.joinUserChannel(channelId);
      fdc3.addContextListener("fdc3.instrument", (context) => {
        setCurrentInstrument(context as Instrument);
      });
    }
  };

  const leaveChannel = async () => {
    if (fdc3) {
      await fdc3.leaveCurrentChannel();
      setCurrentInstrument(null);
    }
  };

  return (
    <div>
      <h3>Canales de Usuario</h3>
      {channels.map((c) => (
        <button
          key={c.id}
          onClick={() => joinChannel(c.id)}
          style={{ backgroundColor: c.displayMetadata.color }}
        >
          {c.displayMetadata.name}
        </button>
      ))}
      <button onClick={leaveChannel}>Salir del Canal</button>
      {currentInstrument && (
        <p>Instrumento actual en el canal: {currentInstrument.id?.ticker}</p>
      )}
    </div>
  );
};

export default ChannelSelector;
```

#### Canales Privados (Private Channels)

Los canales privados ofrecen una comunicación punto a punto y segura. Se crean dinámicamente y se pueden devolver como resultado de un intent, permitiendo una conversación directa entre dos aplicaciones.

**Ejemplo: Creación y uso de un canal privado para streaming de datos**

Aplicación "Servidor" que provee un flujo de datos:

```typescript
// Aplicación que provee el flujo de cotizaciones
useEffect(() => {
  if (fdc3) {
    const listener = fdc3.addIntentListener(
      "GetPriceStream",
      async (context) => {
        const privateChannel = await fdc3.createPrivateChannel();

        // Simula un flujo de precios
        const intervalId = setInterval(() => {
          const priceContext = {
            type: "myorg.price",
            price: Math.random() * 100,
            instrumentId: (context as Instrument).id?.ticker,
          };
          privateChannel.broadcast(priceContext);
        }, 1000);

        privateChannel.onDisconnect(() => {
          clearInterval(intervalId);
        });

        return privateChannel;
      }
    );
    return () => listener.unsubscribe();
  }
}, [fdc3]);
```

Aplicación "Cliente" que consume el flujo de datos:

```typescript
// Aplicación que consume el flujo de cotizaciones
const getPriceStream = async () => {
  if (fdc3) {
    try {
      const instrumentContext: Instrument = {
        type: "fdc3.instrument",
        id: { ticker: "EUR/USD" },
      };
      const resolution = await fdc3.raiseIntent(
        "GetPriceStream",
        instrumentContext
      );
      const privateChannel = await resolution.getResult();

      if (privateChannel && "broadcast" in privateChannel) {
        privateChannel.addContextListener("myorg.price", (priceContext) => {
          console.log("Precio recibido:", priceContext);
        });
      }
    } catch (error) {
      console.error("Error al obtener el flujo de precios:", error);
    }
  }
};
```

---

### Manejo de Errores

La API de FDC3 es asíncrona y basada en promesas, por lo que el manejo de errores es crucial. Utiliza bloques `try...catch` para gestionar los posibles rechazos de las promesas. FDC3 define enumeraciones de errores específicos como `ResolveError` y `ChannelError` que te permiten identificar la causa del fallo.

```typescript
import { ResolveError } from "@finos/fdc3";

const findAndRaiseIntent = async () => {
  if (fdc3) {
    const contactContext = {
      type: "fdc3.contact",
      id: { email: "test@example.com" },
    };
    try {
      // Intenta encontrar aplicaciones que puedan manejar el intent
      const appIntent = await fdc3.findIntent("StartChat", contactContext);
      // Lanza el intent a la primera aplicación encontrada
      await appIntent.raise(contactContext, appIntent.apps[0]);
    } catch (error) {
      if ((error as Error).message === ResolveError.NoAppsFound) {
        alert("No se encontraron aplicaciones para iniciar un chat.");
      } else {
        console.error("Ocurrió un error inesperado:", error);
      }
    }
  }
};
```

Esta guía proporciona una base sólida para desarrollar aplicaciones FDC3 con TypeScript y React. Al aprovechar los contextos, intents y canales, puedes crear flujos de trabajo de usuario potentes e integrados que definen la próxima generación de escritorios financieros. Recuerda siempre consultar la [documentación oficial de FDC3](https://fdc3.finos.org/docs/api/spec) para obtener los detalles más actualizados sobre el estándar.
