The FDC3 standard provides a powerful framework for interoperability between financial applications. While it defines some common contexts and intents, many specialized financial workflows, like those found in Bloomberg TOMS for fixed income, require **custom FDC3 Contexts and Intents**. This allows for precise data exchange and action triggering tailored to specific bond trading operations.

---

## Bloomberg TOMS Functionality Overview

Bloomberg TOMS (Trade Order Management Solutions) is a comprehensive suite for sell-side fixed income firms, offering tools for inventory management, trading, risk, P\&L, compliance, and straight-through processing. We'll focus on these key screens:

- **Trader Workstation**: A real-time blotter and monitoring interface where traders oversee their positions, market activity, P\&L, and manage orders. It provides a consolidated view of their trading book.
- **Trader Ticket**: The order entry and execution screen where traders create, modify, and send orders for various fixed income instruments. It captures trade details, compliance checks, and routes orders for execution.
- **Security Pricing**: A tool for evaluating and analyzing the pricing of specific securities, often incorporating market data, valuation models, and fair value hierarchy leveling.

---

## Custom FDC3 Contexts for Fixed Income

To model the Bloomberg TOMS functionality, we'll define custom FDC3 contexts for corporate bonds and treasuries, extending the standard `fdc3.instrument` type.

### `fdc3.instrument` (Standard FDC3 Context)

The base FDC3 context for any financial instrument.

```json
{
  "type": "fdc3.instrument",
  "id": {
    "ticker": "AAPL",
    "BBG": "AAPL US Equity"
  },
  "name": "Apple Inc."
}
```

### Custom `fx.bond` Context

This context will represent a generic bond, including common identifiers and attributes.

```json
{
  "type": "fx.bond",
  "id": {
    "ISIN": "US912810RA12",
    "CUSIP": "912810RA1",
    "BBG": "T 2 08/15/25 Govt",
    "RIC": "US912810RA12="
  },
  "name": "US Treasury Bond",
  "issueDate": "2020-08-15",
  "maturityDate": "2025-08-15",
  "coupon": 2.0,
  "currency": "USD",
  "issueSize": 1000000000,
  "instrumentType": "Government Bond"
}
```

### Custom `fx.corporateBond` Context

Extends `fx.bond` with attributes specific to corporate bonds.

```json
{
  "type": "fx.corporateBond",
  "id": {
    "ISIN": "US037833AP36",
    "CUSIP": "037833AP3",
    "BBG": "AAPL 0.75 08/20/25 Corp",
    "RIC": "AAPL.075_20250820="
  },
  "name": "Apple Inc. 0.75% 2025 Bond",
  "issueDate": "2020-08-20",
  "maturityDate": "2025-08-20",
  "coupon": 0.75,
  "currency": "USD",
  "issueSize": 1500000000,
  "instrumentType": "Corporate Bond",
  "issuer": {
    "type": "fdc3.organization",
    "id": {
      "LEI": "549300VGE7B0G41T6B54"
    },
    "name": "Apple Inc."
  },
  "rating": "AAA"
}
```

### Custom `fx.treasury` Context

Extends `fx.bond` for US Treasuries.

```json
{
  "type": "fx.treasury",
  "id": {
    "ISIN": "US91282CDU08",
    "CUSIP": "91282CDU0",
    "BBG": "T 4.5 05/15/34 Govt",
    "RIC": "US91282CDU08="
  },
  "name": "US Treasury Bond",
  "issueDate": "2024-05-15",
  "maturityDate": "2034-05-15",
  "coupon": 4.5,
  "currency": "USD",
  "issueSize": 50000000000,
  "instrumentType": "Government Bond"
}
```

### Custom `fx.order` Context

Represents a trading order with specific bond details.

```json
{
  "type": "fx.order",
  "id": {
    "orderId": "ORD-123456"
  },
  "instrument": {
    "type": "fx.corporateBond",
    "id": {
      "ISIN": "US037833AP36"
    },
    "name": "Apple Inc. 0.75% 2025 Bond"
  },
  "side": "Buy",
  "quantity": 1000000,
  "price": 99.5,
  "orderType": "Limit",
  "status": "New",
  "timestamp": "2025-07-15T16:30:00Z"
}
```

### Custom `fx.trade` Context

Represents a executed trade.

```json
{
  "type": "fx.trade",
  "id": {
    "tradeId": "TRD-987654"
  },
  "orderId": "ORD-123456",
  "instrument": {
    "type": "fx.corporateBond",
    "id": {
      "ISIN": "US037833AP36"
    },
    "name": "Apple Inc. 0.75% 2025 Bond"
  },
  "side": "Buy",
  "quantity": 1000000,
  "price": 99.52,
  "executionTime": "2025-07-15T16:35:10Z"
}
```

---

## Custom FDC3 Intents for Fixed Income Workflows

These intents are designed to mimic actions a trader would take within Bloomberg TOMS.

### `fx.viewBondDetails`

- **Description**: Displays detailed information for a specific bond.
- **Contexts Supported**: `fx.bond`, `fx.corporateBond`, `fx.treasury`
- **Analogy to TOMS**: Similar to selecting a bond on the Trader Workstation and viewing its security master data on a Security Pricing-like screen.

### `fx.createOrder`

- **Description**: Initiates the creation of a new trade order for a given bond.
- **Contexts Supported**: `fx.bond`, `fx.corporateBond`, `fx.treasury`
- **Analogy to TOMS**: Equivalent to clicking "New Order" or double-clicking a security on the Trader Workstation to bring up the Trader Ticket.

### `fx.viewOrderBlotter`

- **Description**: Displays a blotter or list of orders, potentially filtered by a specific bond.
- **Contexts Supported**: `fx.bond`, `fx.corporateBond`, `fx.treasury` (optional, for filtering), `fx.order`
- **Analogy to TOMS**: Navigating to or updating the Trader Workstation blotter to show order activity.

### `fx.amendOrder`

- **Description**: Allows modification of an existing trade order.
- **Contexts Supported**: `fx.order`
- **Analogy to TOMS**: Opening an existing order from the blotter on the Trader Ticket for modification.

### `fx.cancelOrder`

- **Description**: Requests cancellation of an outstanding trade order.
- **Contexts Supported**: `fx.order`
- **Analogy to TOMS**: Clicking "Cancel" on an order within the Trader Workstation or Trader Ticket.

### `fx.viewSecurityPricing`

- **Description**: Displays detailed pricing and analytics for a specific bond.
- **Contexts Supported**: `fx.bond`, `fx.corporateBond`, `fx.treasury`
- **Analogy to TOMS**: Opening the "Security Pricing" screen for a selected bond.

### `fx.viewTradeBlotter`

- **Description**: Displays a blotter or list of executed trades, potentially filtered.
- **Contexts Supported**: `fx.bond`, `fx.corporateBond`, `fx.treasury` (optional, for filtering), `fx.trade`
- **Analogy to TOMS**: Navigating to or updating the Trader Workstation blotter to show executed trades.

---

## Detailed Interactions and Workflows

Let's illustrate how these custom contexts and intents would facilitate interoperability between hypothetical applications mimicking Bloomberg TOMS functionality.

### Workflow 1: From Trader Workstation to Trader Ticket (New Order)

**Applications Involved:**

- **Bond Blotter App (Mimicking Trader Workstation)**: Displays a list of corporate bonds and treasuries, along with live market data.
- **Order Entry App (Mimicking Trader Ticket)**: Provides fields to create and submit trade orders.

**Interaction:**

1.  A trader is monitoring the **Bond Blotter App** and sees a corporate bond (e.g., Apple Inc. 0.75% 2025 Bond) they wish to trade.

2.  The trader **selects** this bond in the Bond Blotter App or **clicks a "Trade" button** associated with it.

3.  The Bond Blotter App **raises the `fx.createOrder` intent** with an `fx.corporateBond` context:

    ```javascript
    fdc3.raiseIntent("fx.createOrder", {
      type: "fx.corporateBond",
      id: {
        ISIN: "US037833AP36",
        BBG: "AAPL 0.75 08/20/25 Corp",
      },
      name: "Apple Inc. 0.75% 2025 Bond",
    });
    ```

4.  The FDC3 Desktop Agent resolves the intent, launching or bringing to focus the **Order Entry App**.

5.  The Order Entry App receives the `fx.corporateBond` context, **pre-populating** the instrument details (ISIN, name, etc.) in the new order ticket. The trader then fills in quantity, price, side (Buy/Sell), etc., and submits the order.

---

### Workflow 2: From Order Blotter to Trader Ticket (Amend Order)

**Applications Involved:**

- **Order Blotter App (Mimicking Trader Workstation)**: Shows current and past orders.
- **Order Entry App (Mimicking Trader Ticket)**: Used for order creation and modification.

**Interaction:**

1.  A trader is reviewing outstanding orders in the **Order Blotter App**. They notice an existing order (e.g., ORD-123456) that needs to be amended.

2.  The trader **selects** the specific order in the Order Blotter App.

3.  The Order Blotter App **raises the `fx.amendOrder` intent** with an `fx.order` context:

    ```javascript
    fdc3.raiseIntent("fx.amendOrder", {
      type: "fx.order",
      id: {
        orderId: "ORD-123456",
      },
      instrument: {
        type: "fx.corporateBond",
        id: {
          ISIN: "US037833AP36",
        },
        name: "Apple Inc. 0.75% 2025 Bond",
      },
      side: "Buy",
      quantity: 1000000,
      price: 99.5,
      orderType: "Limit",
      status: "New",
      timestamp: "2025-07-15T16:30:00Z",
    });
    ```

4.  The FDC3 Desktop Agent launches or focuses the **Order Entry App**.

5.  The Order Entry App receives the `fx.order` context, **loading all details of order ORD-123456** into its interface, allowing the trader to modify fields like quantity or price before re-submitting.

---

### Workflow 3: From Any App to Security Pricing Screen

**Applications Involved:**

- **Any App (e.g., News Reader, Blotter, Portfolio Viewer)**: An application that displays or references bonds.
- **Bond Pricing App (Mimicking Security Pricing)**: Dedicated to in-depth bond pricing, analytics, and valuation.

**Interaction:**

1.  A trader is in any application (e.g., a news feed showing a new Treasury issuance or the Bond Blotter App). They see a bond of interest (e.g., a new US Treasury Bond).

2.  The trader **clicks on or selects** the bond within that application.

3.  The source application **raises the `fx.viewSecurityPricing` intent** with an `fx.treasury` or `fx.corporateBond` context:

    ```javascript
    // Example from a news app for a Treasury
    fdc3.raiseIntent("fx.viewSecurityPricing", {
      type: "fx.treasury",
      id: {
        ISIN: "US91282CDU08",
        BBG: "T 4.5 05/15/34 Govt",
      },
      name: "US Treasury Bond",
    });
    ```

4.  The FDC3 Desktop Agent resolves the intent, opening or focusing the **Bond Pricing App**.

5.  The Bond Pricing App receives the bond context, **displaying comprehensive pricing data, yield curves, valuation models, and fair value hierarchy information** for that specific bond.

---

### Workflow 4: Synchronizing Context Across Applications (Channeling)

**Applications Involved:**

- **Bond Blotter App**
- **Security Pricing App**
- **Order Entry App**
- **Risk Dashboard App (New hypothetical app)**: Shows real-time risk metrics for a selected instrument.

**Interaction:**

1.  All four applications **join a common FDC3 Channel** (e.g., "Green Channel").

2.  The trader selects a corporate bond in the **Bond Blotter App**.

3.  The Bond Blotter App **broadcasts an `fx.corporateBond` context** to the active channel:

    ```javascript
    fdc3.broadcast({
      type: "fx.corporateBond",
      id: {
        ISIN: "US037833AP36",
        BBG: "AAPL 0.75 08/20/25 Corp",
      },
      name: "Apple Inc. 0.75% 2025 Bond",
    });
    ```

4.  The **Security Pricing App**, **Order Entry App**, and **Risk Dashboard App** are all listening on the "Green Channel" for `fx.corporateBond` contexts.

5.  Upon receiving the broadcast, each of these applications **automatically updates its display** to show data relevant to the "Apple Inc. 0.75% 2025 Bond".

    - The **Security Pricing App** shows its pricing and analytics.
    - The **Order Entry App** prepares a new ticket for that bond.
    - The **Risk Dashboard App** updates to show the risk exposure related to that specific bond.

This channel-based interaction streamlines the trader's workflow by ensuring that all relevant applications are always in sync with the instrument of current focus, significantly reducing manual data entry and navigation.
