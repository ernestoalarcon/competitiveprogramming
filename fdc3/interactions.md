¡Entendido! Vamos a explorar cómo utilizar la API de FDC3 con TypeScript de manera detallada. FDC3 (Financial Desktop Connectivity and Collaboration Consortium) es un estándar abierto que permite la interoperabilidad entre aplicaciones en entornos financieros, facilitando acciones como compartir contexto, lanzar aplicaciones y manejar intenciones (intents). A continuación, te guiaré paso a paso para configurar y usar la API de FDC3 en un proyecto con TypeScript, incluyendo ejemplos prácticos y explicaciones.

---

### **1. Introducción a FDC3**

FDC3 proporciona una API estandarizada para que las aplicaciones en un escritorio financiero puedan interoperar. Esto incluye:

- **Intents**: Permiten a una aplicación solicitar una acción específica a otra (por ejemplo, "mostrar un gráfico" o "iniciar un chat").
- **Contextos**: Objetos de datos que representan información compartida entre aplicaciones (por ejemplo, un instrumento financiero como `fdc3.instrument`).
- **Canales (Channels)**: Mecanismos para compartir contexto entre aplicaciones en tiempo real.
- **Desktop Agent**: Un componente que actúa como intermediario para coordinar estas interacciones.

La API de FDC3 está diseñada para ser independiente del lenguaje, pero en este caso nos enfocaremos en su uso con TypeScript, que es compatible con los entornos web y de escritorio.

---

### **2. Configuración del entorno**

#### **2.1. Requisitos previos**

- **Node.js y npm**: Asegúrate de tener Node.js instalado (versión recomendada: LTS, como 18.x o superior).
- **TypeScript**: Instala TypeScript globalmente o en tu proyecto:
  ```bash
  npm install -g typescript
  ```
  O localmente en el proyecto:
  ```bash
  npm install --save-dev typescript
  ```
- **Un Desktop Agent compatible con FDC3**: Necesitas un entorno que proporcione una implementación del Desktop Agent, como OpenFin, Finsemble, o un agente personalizado. Si estás en un entorno web, puedes usar el paquete `@finos/fdc3`.

#### **2.2. Crear un proyecto TypeScript**

1. Crea un nuevo directorio para tu proyecto y inicialízalo:
   ```bash
   mkdir fdc3-typescript-example
   cd fdc3-typescript-example
   npm init -y
   ```
2. Instala TypeScript y el paquete `@finos/fdc3`:
   ```bash
   npm install @finos/fdc3
   npm install --save-dev typescript ts-node
   ```
3. Configura TypeScript creando un archivo `tsconfig.json`:
   ```json
   {
     "compilerOptions": {
       "target": "ES2020",
       "module": "CommonJS",
       "strict": true,
       "esModuleInterop": true,
       "outDir": "./dist",
       "rootDir": "./src",
       "sourceMap": true
     },
     "include": ["src/**/*"],
     "exclude": ["node_modules"]
   }
   ```
4. Crea una carpeta `src` y un archivo inicial, por ejemplo, `index.ts`.

---

### **3. Conexión al Desktop Agent**

Para usar FDC3 en TypeScript, primero debes conectar tu aplicación a un Desktop Agent. Esto se hace a través de la función `getAgent()` o verificando la disponibilidad de `window.fdc3`.

#### **3.1. Verificar si FDC3 está listo**

El evento `fdc3Ready` indica que la API de FDC3 está disponible. Puedes usar la función `fdc3Ready` del paquete `@finos/fdc3` para esperar a que el Desktop Agent esté listo.

```typescript
import { fdc3Ready } from "@finos/fdc3";

async function initializeFDC3() {
  try {
    await fdc3Ready();
    console.log("FDC3 está listo!");
    // Aquí puedes empezar a usar la API de FDC3
  } catch (error) {
    console.error("Error al conectar con el Desktop Agent:", error);
  }
}

initializeFDC3();
```

**Explicación**:

- `fdc3Ready()` devuelve una promesa que se resuelve cuando el objeto `window.fdc3` está disponible.
- Si el Desktop Agent no está disponible, se lanzará un error, como `AgentNotFound` (ver).[](https://fdc3.finos.org/docs/api/ref/Errors)

#### **3.2. Usar `getAgent` (Opcional para entornos web)**

Si estás trabajando en un entorno web donde el Desktop Agent no está pre-inyectado en `window.fdc3`, puedes usar `getAgent()` para conectar con un agente residente en el navegador o en un iframe.

```typescript
import { getAgent } from "@finos/fdc3";

async function connectToAgent() {
  try {
    const desktopAgent = await getAgent();
    console.log("Conectado al Desktop Agent:", desktopAgent);
    // Ahora puedes usar desktopAgent para interactuar con la API
  } catch (error) {
    console.error("Error al obtener el Desktop Agent:", error);
  }
}

connectToAgent();
```

**Nota**: `getAgent()` implementa el Web Connection Protocol (WCP) y puede conectar con un Desktop Agent a través de `postMessage` o un iframe (ver).[](https://fdc3.finos.org/docs/next/api/specs/webConnectionProtocol)

---

### **4. Usando la API de FDC3**

#### **4.1. Abrir una aplicación (`fdc3.open`)**

La función `fdc3.open` permite lanzar una aplicación específica usando un `AppIdentifier`.

```typescript
import { fdc3Ready } from "@finos/fdc3";

async function openApp() {
  await fdc3Ready();
  try {
    const appIdentifier = { appId: "my-chart-app" }; // Identificador de la aplicación
    await window.fdc3.open(appIdentifier, {
      type: "fdc3.instrument",
      id: { ticker: "AAPL" },
    });
    console.log("Aplicación abierta con éxito");
  } catch (error) {
    console.error("Error al abrir la aplicación:", error);
  }
}

openApp();
```

**Explicación**:

- `appId` es un identificador único para la aplicación, definido en un directorio de aplicaciones (App Directory).
- Puedes pasar un contexto (por ejemplo, `fdc3.instrument`) para compartir datos con la aplicación que se abre.
- Errores comunes incluyen `AppNotFound` o `AppTimeout` si la aplicación no responde (ver).[](https://fdc3.finos.org/docs/api/ref/Errors)

#### **4.2. Manejar Intents (`fdc3.raiseIntent` y `addIntentListener`)**

Los **intents** permiten a una aplicación solicitar una acción específica a otra aplicación.

**Ejemplo: Enviar un intent**

```typescript
import { fdc3Ready } from "@finos/fdc3";

async function raiseIntent() {
  await fdc3Ready();
  try {
    const context = {
      type: "fdc3.instrument",
      id: { ticker: "AAPL" },
    };
    const resolution = await window.fdc3.raiseIntent("ViewChart", context);
    console.log("Intent resuelto:", resolution);
  } catch (error) {
    console.error("Error al enviar el intent:", error);
  }
}

raiseIntent();
```

**Ejemplo: Escuchar un intent**

```typescript
import { fdc3Ready, addIntentListener } from "@finos/fdc3";

async function setupIntentListener() {
  await fdc3Ready();
  const listener = addIntentListener("ViewChart", (context) => {
    console.log("Intent recibido con contexto:", context);
    // Procesar el contexto, por ejemplo, mostrar un gráfico para el instrumento
    return { type: "fdc3.chart", id: { ticker: context.id.ticker } }; // Retornar un resultado opcional
  });
  console.log("Escuchando el intent ViewChart");
}

setupIntentListener();
```

**Explicación**:

- `raiseIntent` envía una solicitud a un Desktop Agent para que otra aplicación resuelva el intent `ViewChart` con el contexto proporcionado.
- `addIntentListener` permite a tu aplicación escuchar intents específicos y procesar el contexto recibido.
- Los intents pueden devolver datos (ver), y TypeScript permite usar genéricos para tipar el resultado, como `fdc3.raiseIntent<TradeResult>`.[](https://github.com/finos/FDC3/issues/201)

#### **4.3. Compartir contexto a través de canales**

Los canales permiten compartir contexto entre aplicaciones en tiempo real.

**Ejemplo: Unirse a un canal y transmitir contexto**

```typescript
import { fdc3Ready } from "@finos/fdc3";

async function joinChannel() {
  await fdc3Ready();
  try {
    const channel = await window.fdc3.getOrCreateChannel("my-channel");
    const context = {
      type: "fdc3.contact",
      id: { email: "user@example.com" },
    };
    await channel.broadcast(context);
    console.log("Contexto transmitido al canal:", context);
  } catch (error) {
    console.error("Error al trabajar con el canal:", error);
  }
}

joinChannel();
```

**Ejemplo: Escuchar contexto en un canal**

```typescript
import { fdc3Ready } from "@finos/fdc3";

async function listenToChannel() {
  await fdc3Ready();
  try {
    const channel = await window.fdc3.getOrCreateChannel("my-channel");
    channel.addContextListener("fdc3.contact", (context) => {
      console.log("Contexto recibido en el canal:", context);
      // Procesar el contexto, por ejemplo, actualizar una UI
    });
    console.log("Escuchando contexto en el canal my-channel");
  } catch (error) {
    console.error("Error al escuchar el canal:", error);
  }
}

listenToChannel();
```

**Explicación**:

- `getOrCreateChannel` crea o se une a un canal identificado por un ID único.
- `broadcast` envía un contexto a todas las aplicaciones suscritas al canal.
- `addContextListener` permite escuchar contextos específicos (por ejemplo, `fdc3.contact`) en el canal.
- Los contextos deben tener un campo `type` obligatorio (ver).[](https://fdc3.finos.org/docs/api/ref/Types)

---

### **5. Tipado en TypeScript**

El paquete `@finos/fdc3` incluye definiciones de TypeScript generadas a partir de esquemas JSON (ver). Algunos tipos clave son:[](https://github.com/finos/FDC3)

- `AppIdentifier`: `{ appId: string; instanceId?: string }` para identificar aplicaciones.
- `Context`: Interfaz base para contextos, con un campo `type` obligatorio.
- `IntentResolution`: Retornado por `raiseIntent`, incluye información sobre la aplicación que resolvió el intent.
- `Channel`: Interfaz para interactuar con canales.

Puedes importar tipos específicos para un tipado más robusto:

```typescript
import { Context, AppIdentifier, IntentResolution } from "@finos/fdc3";

const context: Context = {
  type: "fdc3.instrument",
  id: { ticker: "AAPL" },
};

async function openAppWithIdentifier(app: AppIdentifier) {
  const resolution: IntentResolution = await window.fdc3.raiseIntent(
    "ViewChart",
    context,
    app
  );
  console.log("Resolución:", resolution);
}
```

---

### **6. Manejo de errores**

FDC3 define enumeraciones de errores específicas (ver), como:[](https://fdc3.finos.org/docs/api/ref/Errors)

- `AgentError`: Para errores al conectar con el Desktop Agent (`AgentNotFound`, `AccessDenied`).
- `ChannelError`: Para errores relacionados con canales (`NoChannelFound`, `MalformedContext`).
- `OpenError`: Para errores al abrir aplicaciones (`AppNotFound`, `AppTimeout`).

Siempre usa bloques `try/catch` para manejar estos errores:

```typescript
try {
  await window.fdc3.open({ appId: "non-existent-app" });
} catch (error) {
  if (error.message === "AppNotFound") {
    console.error("La aplicación no se encontró");
  } else {
    console.error("Error desconocido:", error);
  }
}
```

---

### **7. Buenas prácticas**

1. **Usa contextos estándar**: Prefiere contextos definidos por FDC3 (como `fdc3.instrument`, `fdc3.contact`) sobre contextos propietarios (ver).[](https://fdc3.finos.org/docs/next/context/spec)
2. **Espera a `fdc3Ready`**: Siempre verifica que el Desktop Agent esté listo antes de usar la API.
3. **Maneja timeouts**: Configura listeners de contexto o intents dentro de los 15 segundos después del lanzamiento para evitar errores de timeout (ver).[](https://fdc3.finos.org/docs/2.1/api/spec)
4. **Prueba en un entorno real**: Usa un Desktop Agent como OpenFin o Finsemble para pruebas, ya que el comportamiento puede variar.
5. **Consulta la documentación**: Los esquemas JSON y las definiciones de TypeScript están en el repositorio de FDC3 (https://github.com/finos/FDC3).

---

### **8. Ejemplo completo**

Aquí tienes un ejemplo completo que combina varias funcionalidades:

```typescript
import { fdc3Ready, addIntentListener, getAgent } from "@finos/fdc3";
import type { Context, IntentResolution } from "@finos/fdc3";

async function initializeApp() {
  try {
    // Esperar a que FDC3 esté listo
    await fdc3Ready();
    console.log("FDC3 está listo");

    // Unirse a un canal y transmitir contexto
    const channel = await window.fdc3.getOrCreateChannel("my-channel");
    const context: Context = {
      type: "fdc3.instrument",
      id: { ticker: "AAPL" },
    };
    await channel.broadcast(context);
    console.log("Contexto transmitido:", context);

    // Escuchar contexto en el canal
    channel.addContextListener("fdc3.instrument", (ctx) => {
      console.log("Contexto recibido:", ctx);
    });

    // Escuchar un intent
    addIntentListener("ViewChart", (ctx: Context) => {
      console.log("Intent ViewChart recibido:", ctx);
      return { type: "fdc3.chart", id: { ticker: ctx.id.ticker } };
    });

    // Enviar un intent
    const resolution: IntentResolution = await window.fdc3.raiseIntent(
      "ViewChart",
      context
    );
    console.log("Intent resuelto:", resolution);
  } catch (error) {
    console.error("Error en la aplicación:", error);
  }
}

initializeApp();
```

---

### **9. Recursos adicionales**

- **Documentación oficial**: [fdc3.finos.org](https://fdc3.finos.org)
- **Repositorio de FDC3**: [github.com/finos/FDC3](https://github.com/finos/FDC3)
- **Paquete npm**: [npmjs.com/package/@finos/fdc3](https://www.npmjs.com/package/@finos/fdc3)
- **Comunidad**: Únete al canal `#fdc3` en el Slack de FINOS o contacta a `fdc3@finos.org` para soporte.

---

### **10. Consideraciones finales**

- **Entornos de prueba**: Si no tienes un Desktop Agent, puedes usar el proyecto FDC3 Sail (ver) o probar en un entorno como OpenFin.[](https://github.com/finos/FDC3)
- **Interoperabilidad**: FDC3 está diseñado para ser independiente de la plataforma, pero asegúrate de que tu Desktop Agent cumpla con la versión de FDC3 que estás usando (por ejemplo, 2.1 o 2.2).
- **Web vs. Nativo**: En entornos web, considera el Web Connection Protocol (WCP) para conectar con agentes residentes en el navegador (ver).[](https://fdc3.finos.org/docs/next/api/specs/webConnectionProtocol)

Si necesitas más detalles sobre un caso de uso específico o ayuda con un Desktop Agent en particular, no dudes en preguntar. ¡Espero que esta guía te sea útil! 🚀
