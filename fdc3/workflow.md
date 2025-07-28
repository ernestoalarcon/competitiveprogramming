Claro. Para modelar la funcionalidad de un sistema de gestión de órdenes (OMS) como Bloomberg TOMS enfocado en bonos corporativos y treasuries, es necesario extender el estándar FDC3 con `Contexts` e `Intents` específicos. A continuación, se detalla un modelo de casos de uso, las definiciones custom y el flujo de interacción entre aplicaciones.

---

### \#\# 1. Casos de Uso y Workflows

Modelaremos tres flujos de trabajo principales que un trader de renta fija realizaría, involucrando distintas aplicaciones en su escritorio digital.

#### **Caso de Uso 1: Análisis Pre-Trade desde la Estación de Trabajo**

1.  **Inicio:** El trader está en su aplicación principal, la **"Trader Workstation"**. Esta pantalla muestra un resumen de sus posiciones actuales, P\&L (Profit and Loss), y una lista de seguimiento de bonos de interés.
2.  **Acción:** El trader ve que un bono específico (ej. un Treasury a 10 años) en su lista de seguimiento ha alcanzado un precio interesante. Hace clic en el bono para analizarlo en detalle.
3.  **Interacción FDC3:** La "Trader Workstation" emite un `Intent` para ver los detalles de precios de ese bono.
4.  **Resultado:** Una aplicación especializada de **"Security Pricing"** se abre o se enfoca, mostrando en tiempo real el precio, el rendimiento (yield), el spread, y métricas de riesgo clave (como duración y convexidad) para ese bono.
5.  **Siguiente Acción:** Después de analizarlo, el trader decide que quiere poner una orden de compra. Desde la aplicación de "Security Pricing", hace clic en un botón "Operar" (Trade).
6.  **Interacción FDC3:** La aplicación de "Security Pricing" emite un `Intent` para crear una orden para ese instrumento.
7.  **Resultado:** Se abre la aplicación **"Trader Ticket"** con los detalles del bono ya precargados (ISIN, CUSIP, nombre).

#### **Caso de Uso 2: Ejecución de la Orden**

1.  **Inicio:** El trader está en la aplicación **"Trader Ticket"**, que ya tiene la información del bono.
2.  **Acción:** El trader completa los detalles de la orden:
    - **Dirección:** Compra (Buy).
    - **Cantidad:** 25,000,000 USD.
    - **Tipo de Orden:** Límite por Rendimiento (Limit by Yield).
    - **Rendimiento Límite:** 4.25%.
    - **Contraparte:** Selecciona una de una lista.
3.  **Interacción FDC3:** Una vez que el trader hace clic en "Ejecutar", la aplicación "Trader Ticket" emite un `Intent` para ejecutar la orden.
4.  **Resultado:** La orden es enviada al mercado o a un sistema de ejecución. La aplicación "Trader Ticket" recibe una confirmación.
5.  **Siguiente Acción:** Tras la confirmación, la aplicación "Trader Ticket" necesita informar al resto del ecosistema sobre la nueva operación y la posición actualizada.
6.  **Interacción FDC3:** La aplicación **difunde (`broadcast`)** un nuevo `Context` de posición actualizado en el canal del trader.

#### **Caso de Uso 3: Actualización Post-Trade y Sincronización**

1.  **Inicio:** La operación ha sido ejecutada.
2.  **Acción (Automática):** La **"Trader Workstation"**, que está escuchando en el mismo canal FDC3, recibe el nuevo `Context` de posición.
3.  **Resultado:** La "Trader Workstation" actualiza instantáneamente la vista de posiciones del trader, reflejando la nueva cantidad del bono, el precio promedio de la posición y el P\&L no realizado. Una aplicación de **"Análisis de Riesgo"** también podría estar escuchando y recalcular la exposición general del trader en tiempo real.

---

### \#\# 2. Definiciones Custom de Contexts e Intents FDC3

Para soportar estos workflows, necesitamos extender los objetos estándar de FDC3. Usaremos un prefijo `toms.` para indicar que son customizaciones para nuestro sistema de Trade Order Management.

#### **Contexts Custom**

Estos contextos extienden los tipos estándar de FDC3 (`fdc3.instrument`, `fdc3.order`, `fdc3.position`) para añadir campos específicos de bonos.

**1. `toms.instrument.bond`**
Hereda de `fdc3.instrument` y añade datos cruciales para bonos.

```json
{
  "type": "toms.instrument.bond",
  "name": "US Treasury Note 4.500% 15-May-2034",
  "id": {
    "isin": "US91282CJZ59",
    "cusip": "91282CJZ5",
    "figi": "BBG01P4Z2W38"
  },
  "market": {
    "yield": 4.235,
    "spread": 0.052,
    "price": 101.5
  },
  "specs": {
    "maturity": "2034-05-15",
    "coupon": 4.5,
    "rating": "AA+",
    "faceValue": 1000,
    "issueDate": "2024-05-15"
  }
}
```

**2. `toms.order.bond`**
Hereda de `fdc3.order` para manejar órdenes de bonos que pueden ser por precio o por rendimiento.

```json
{
  "type": "toms.order.bond",
  "instrument": {
    "type": "toms.instrument.bond",
    "id": { "isin": "US91282CJZ59" }
  },
  "quantity": 25000000,
  "side": "buy",
  "orderType": "Yield", // Puede ser 'Price' o 'Yield'
  "limitYield": 4.25, // Usado si orderType es 'Yield'
  "limitPrice": null, // Usado si orderType es 'Price'
  "counterparty": {
    "type": "fdc3.organization",
    "name": "Major Dealer Bank",
    "id": { "lei": "5493001B3S3D3KJR4B82" }
  },
  "settlementDate": "2025-07-17"
}
```

**3. `toms.position.bond`**
Hereda de `fdc3.position` para incluir P\&L y valor de mercado.

```json
{
  "type": "toms.position.bond",
  "instrument": {
    "type": "toms.instrument.bond",
    "id": { "isin": "US91282CJZ59" }
  },
  "holding": 75000000, // Cantidad total en la posición
  "costBasis": 101.25, // Precio promedio de compra
  "marketValue": 76125000, // holding * marketPrice
  "unrealizedPnL": 187500
}
```

#### **Intents Custom**

Estos son los verbos o acciones que las aplicaciones pueden solicitar.

**1. `ViewBondPricing`**

- **Descripción:** Solicita a una aplicación que muestre información detallada de precios y mercado para un bono.
- **Contexto Esperado:** `toms.instrument.bond`
- **Ejemplo de uso:** El trader hace clic en un bono en la Workstation, y esta "levanta" el intent `ViewBondPricing`.

**2. `CreateBondOrder`**

- **Descripción:** Abre un ticket de orden para un bono específico, precargando sus datos.
- **Contexto Esperado:** `toms.instrument.bond`
- **Ejemplo de uso:** Desde la pantalla de precios, el trader decide operar y la aplicación "levanta" el intent `CreateBondOrder`.

**3. `ExecuteBondOrder`**

- **Descripción:** Envía una orden de bono completa para su ejecución.
- **Contexto Esperado:** `toms.order.bond`
- **Ejemplo de uso:** El trader hace clic en "Ejecutar" en el Trader Ticket.

---

### \#\# 3. Flujo Detallado de Interacciones FDC3

Aquí se describe cómo los `Contexts` e `Intents` conectan las aplicaciones en el workflow.

**Paso 1: Del Workstation al Análisis de Precios** 📈

1.  La aplicación **Trader Workstation** tiene una lista de instrumentos. Cuando el trader hace clic en el Treasury a 10 años, la aplicación prepara el contexto `toms.instrument.bond`.
2.  La Workstation ejecuta el siguiente código FDC3:
    ```javascript
    const bondContext = {
      type: "toms.instrument.bond",
      name: "US Treasury Note 4.500% 15-May-2034",
      id: { isin: "US91282CJZ59" },
    };
    await fdc3.raiseIntent("ViewBondPricing", bondContext);
    ```
3.  El FDC3 Desktop Agent busca qué aplicación ha registrado el `Intent` `ViewBondPricing`. Encuentra la aplicación **Security Pricing**.
4.  La aplicación **Security Pricing** se abre o enfoca, recibe el `bondContext`, y usa el `isin` para suscribirse a datos de mercado en tiempo real y mostrar toda la información relevante.

**Paso 2: Del Análisis de Precios al Ticket de Orden** 🎟️

1.  En la aplicación **Security Pricing**, el trader presiona el botón "Operar".
2.  Esta aplicación ya tiene el contexto del bono. Ejecuta:
    ```javascript
    // 'currentBondContext' es el contexto que la app está mostrando
    await fdc3.raiseIntent("CreateBondOrder", currentBondContext);
    ```
3.  El Desktop Agent resuelve este `Intent` y lanza la aplicación **Trader Ticket**.
4.  El **Trader Ticket** recibe el `currentBondContext` y precarga los campos del instrumento (ISIN, nombre, etc.), dejando que el trader se enfoque en los detalles de la orden (cantidad, dirección, etc.).

**Paso 3: Ejecución y Broadcast de la Actualización** 📡

1.  El trader llena el **Trader Ticket** y presiona "Ejecutar". La aplicación internamente crea el contexto `toms.order.bond`.
2.  Primero, podría levantar un `Intent` para la ejecución real:
    ```javascript
    const bondOrderContext = {
      /* ...datos de la orden... */
    };
    await fdc3.raiseIntent("ExecuteBondOrder", bondOrderContext);
    ```
    _Nota: Un sistema de ejecución podría escuchar este intent para procesar la orden._
3.  Tras recibir la confirmación de ejecución, el **Trader Ticket** debe notificar a todo el escritorio. Para esto, usa `fdc3.broadcast`. Se asume que las aplicaciones del trader están unidas al mismo canal (ej. "Trader Channel 1").
4.  La aplicación crea el nuevo contexto `toms.position.bond` y lo difunde:
    ```javascript
    const newPositionContext = {
      type: "toms.position.bond",
      instrument: {
        type: "toms.instrument.bond",
        id: { isin: "US91282CJZ59" },
      },
      holding: 75000000,
      /* ... otros campos de la posición ... */
    };
    await fdc3.broadcast(newPositionContext);
    ```
5.  La **Trader Workstation** y cualquier otra aplicación suscrita (como una de riesgo) reciben este contexto a través de su `listener` FDC3. Al ver que el `type` es `toms.position.bond`, saben cómo procesarlo y actualizan sus vistas de inmediato, completando el ciclo de manera fluida y en tiempo real.
