Claro, aquí tienes ejemplos detallados de cómo usar tu `FDC3Model` para escuchar intents y para gestionar un stream de datos a través de un canal privado, todo dentro de componentes React.

---

### 👂 Escuchar un Intent en React

Para que tu aplicación reaccione a un intent lanzado por otra aplicación (por ejemplo, `ViewContact`), debes registrar un _listener_. El mejor lugar para hacer esto en React es dentro de un hook `useEffect` para asegurar que el listener se registre cuando el componente se monta y se elimine cuando se desmonta.

Aquí tienes un componente `ContactViewer` que espera a que otra aplicación le pida mostrar los detalles de un contacto.

#### **`src/components/ContactViewer.tsx`**

```typescript
import React, { useState, useEffect } from "react";
import { useFDC3 } from "../hooks/useFDC3";
import { Contact, Listener } from "@finos/fdc3";

const ContactViewer: React.FC = () => {
  const fdc3 = useFDC3();
  const [activeContact, setActiveContact] = useState<Contact | null>(null);

  useEffect(() => {
    let intentListener: Listener;

    const setupIntentListener = async () => {
      console.log('Registrando listener para el intent "ViewContact"...');

      // Usa FDC3Model para registrar el listener
      intentListener = await fdc3.addIntentListener<Contact>(
        "ViewContact",
        (contact) => {
          console.log(`Intent 'ViewContact' recibido:`, contact);
          setActiveContact(contact);
          // Opcional: Podrías traer la ventana de tu app al frente aquí
        }
      );
    };

    setupIntentListener().catch(console.error);

    // Función de limpieza: Es CRÍTICO desuscribirse para evitar memory leaks
    return () => {
      if (intentListener) {
        console.log('Eliminando listener para "ViewContact".');
        intentListener.unsubscribe();
      }
    };
  }, [fdc3]); // El efecto se ejecuta solo cuando 'fdc3' está disponible

  return (
    <div
      style={{ border: "1px solid #00a8e8", padding: "10px", margin: "10px" }}
    >
      <h4>👤 Visor de Contactos (Escuchando 'ViewContact')</h4>
      {activeContact ? (
        <div>
          <p>
            <strong>Nombre:</strong> {activeContact.name}
          </p>
          <p>
            <strong>Email:</strong> {activeContact.id?.email}
          </p>
        </div>
      ) : (
        <p>Esperando que un intent 'ViewContact' sea lanzado...</p>
      )}
    </div>
  );
};

export default ContactViewer;
```

---

### ⚡ Streaming de Datos con Canales Privados

Este es un patrón poderoso para flujos de trabajo de solicitud/respuesta donde la respuesta es un stream continuo de datos (ej. precios, noticias, etc.). El flujo es el siguiente:

1.  **Consumidor**: Lanza un intent, como `GetPriceStream`.
2.  **Proveedor**: Escucha ese intent, crea un **canal privado**, y devuelve el canal como resultado del intent.
3.  **Proveedor**: Comienza a difundir datos (precios) en ese canal privado.
4.  **Consumidor**: Recibe el canal privado y empieza a escuchar los datos que llegan por él.

#### 1\. Componente Proveedor (El que envía el stream)

Este componente escucha el intent y crea el canal privado.

**`src/components/PriceStreamProvider.tsx`**

```typescript
import React, { useEffect } from "react";
import { useFDC3 } from "../hooks/useFDC3";
import { Instrument, Listener, PrivateChannel } from "@finos/fdc3";

const PriceStreamProvider: React.FC = () => {
  const fdc3 = useFDC3();

  useEffect(() => {
    let intentListener: Listener;

    const setupProvider = async () => {
      // Registrar el listener para el intent que iniciará el stream
      intentListener = await fdc3.addIntentListener(
        "GetPriceStream",
        async (instrument: Instrument) => {
          console.log(
            `Petición de stream de precios recibida para: ${instrument.id?.ticker}`
          );

          // 1. Crear el canal privado usando FDC3Model
          const privateChannel = await fdc3.createPrivateChannel();

          // 2. Iniciar el stream de datos simulado en el canal privado
          const intervalId = setInterval(() => {
            const priceContext = {
              type: "myorg.price",
              price: (Math.random() * 100).toFixed(2),
              ticker: instrument.id?.ticker,
            };
            privateChannel.broadcast(priceContext);
          }, 1500);

          // 3. Manejar la desconexión para limpiar el intervalo
          privateChannel.onDisconnect(() => {
            console.log(
              `El consumidor para ${instrument.id?.ticker} se ha desconectado. Deteniendo stream.`
            );
            clearInterval(intervalId);
          });

          // 4. Retornar el canal al consumidor INMEDIATAMENTE
          return privateChannel;
        }
      );
    };

    setupProvider().catch(console.error);

    return () => {
      if (intentListener) {
        intentListener.unsubscribe();
      }
    };
  }, [fdc3]);

  return (
    <div
      style={{ border: "1px solid #3c40c6", padding: "10px", margin: "10px" }}
    >
      <h4>📈 Proveedor de Streams de Precios</h4>
      <p>Listo para recibir peticiones 'GetPriceStream'.</p>
    </div>
  );
};

export default PriceStreamProvider;
```

#### 2\. Componente Consumidor (El que pide y recibe el stream)

Este componente tiene un botón para pedir el stream y luego muestra los datos recibidos.

**`src/components/PriceStreamConsumer.tsx`**

```typescript
import React, { useState } from "react";
import { useFDC3 } from "../hooks/useFDC3";
import { Instrument, Context, PrivateChannel } from "@finos/fdc3";

// Definimos el tipo de contexto de precio para type-safety
interface PriceContext extends Context {
  type: "myorg.price";
  price: string;
  ticker?: string;
}

const PriceStreamConsumer: React.FC = () => {
  const fdc3 = useFDC3();
  const [prices, setPrices] = useState<PriceContext[]>([]);
  const [subscribedTicker, setSubscribedTicker] = useState<string>("");

  const handleRequestStream = async (ticker: string) => {
    try {
      setPrices([]); // Limpiar precios anteriores
      setSubscribedTicker(ticker);

      const instrument: Instrument = {
        type: "fdc3.instrument",
        id: { ticker },
      };

      // 1. Lanzar el intent para pedir el stream
      const resolution = await fdc3.raiseIntent("GetPriceStream", instrument);

      // 2. Obtener el canal privado del resultado del intent
      const privateChannel = (await resolution.getResult()) as PrivateChannel;

      // 3. Verificar que obtuvimos un canal válido y escuchar el contexto de precios
      if (
        privateChannel &&
        typeof privateChannel.addContextListener === "function"
      ) {
        privateChannel.addContextListener<PriceContext>(
          "myorg.price",
          (price) => {
            setPrices((prevPrices) => [price, ...prevPrices.slice(0, 4)]); // Mantener solo los últimos 5 precios
          }
        );
      } else {
        throw new Error(
          "La resolución del intent no retornó un canal privado válido."
        );
      }
    } catch (error) {
      console.error(`Error al solicitar el stream para ${ticker}:`, error);
      setSubscribedTicker("");
    }
  };

  return (
    <div
      style={{ border: "1px solid #ffa801", padding: "10px", margin: "10px" }}
    >
      <h4>💵 Consumidor de Streams de Precios</h4>
      <button onClick={() => handleRequestStream("AAPL")}>
        Obtener Precios de AAPL
      </button>
      <button onClick={() => handleRequestStream("TSLA")}>
        Obtener Precios de TSLA
      </button>

      {subscribedTicker && <h4>Precios para {subscribedTicker}:</h4>}
      <ul>
        {prices.map((p, i) => (
          <li key={i}>${p.price}</li>
        ))}
      </ul>
    </div>
  );
};

export default PriceStreamConsumer;
```
