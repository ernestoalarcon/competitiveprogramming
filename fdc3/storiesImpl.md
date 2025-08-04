Excellent. Based on the scenarios and use cases, here is a set of FDC3 Contexts and Intents to implement the described workflows, focusing on the interoperability between the standalone **Workspace**, **Ticket**, and **Pricing** applications.

### FDC3 for Application Interoperability

Using FDC3 (Fintech Desktop Connectivity and Collaboration Consortium) allows your three independent applications to act as one cohesive unit on the user's desktop. By passing standardized `Context` data and raising `Intents`, one application can request another to perform an action, creating seamless workflows without being tightly coupled. For example, a Trader can click on a position in the **Workspace** and have the **Pricing** app instantly show the rules for that specific bond.

---

### Custom FDC3 Contexts

We will define custom context types to represent the specific data objects in your application. They follow the `namespace.type` convention.

#### **1. `toms.order`**

This is the core context object representing a trade order. It will be passed between the **Ticket** and **Workspace** applications during the negotiation workflow.

- **Purpose:** To encapsulate all details of a buy/sell order.
- **Used In:** The entire order negotiation lifecycle (Use Cases 1.1, 1.2).

<!-- end list -->

```json
{
  "type": "toms.order",
  "id": { "orderId": "ORD-20250804-105" },
  "instrument": {
    "type": "fdc3.instrument",
    "id": { "CUSIP": "912828U40" }
  },
  "book": "CORP_HY_TRD",
  "counterparty": {
    "type": "fdc3.contact",
    "id": { "email": "buyer@bigfund.com" },
    "name": "Big Asset Management"
  },
  "salesperson": {
    "type": "fdc3.contact",
    "id": { "email": "sarah.sales@yourbank.com" },
    "name": "Sarah Sales"
  },
  "details": {
    "side": "Buy",
    "quantity": 10000000,
    "price": 99.85,
    "priceSource": "Trader",
    "status": "PendingPrice", // PendingPrice, Priced, Confirmed, Cancelled, Rejected
    "notes": "Client is eager to buy before noon."
  }
}
```

#### **2. `toms.position`**

This context represents a specific position held in a book, as displayed on the **Workspace**.

- **Purpose:** To allow the user to select a position and view related information (like pricing rules or constituent trades) in another application.
- **Used In:** Workspace monitoring and drill-down (Use Case 3.2).

<!-- end list -->

```json
{
  "type": "toms.position",
  "instrument": {
    "type": "fdc3.instrument",
    "id": { "CUSIP": "037833100" }
  },
  "book": "CORP_IG_TRD",
  "details": {
    "quantity": 25000000,
    "marketValue": 25125000,
    "pnl": 52000
  }
}
```

#### **3. `toms.pricingRule`**

This context represents a pricing rule configured in the **Pricing** screen.

- **Purpose:** While rules are primarily used internally, this context could be broadcasted to inform other tools (like a risk dashboard) of a new active rule. Its main use here is as the context for the `ViewPrice` intent.
- **Used In:** Pricing setup and viewing (Use Case 2.1).

<!-- end list -->

```json
{
  "type": "toms.pricingRule",
  "instrument": {
    "type": "fdc3.instrument",
    "id": { "CUSIP": "912828U40" }
  },
  "ruleId": "PR-MATRIX-UST5Y-50",
  "ruleType": "Matrix", // Manual, Source, Matrix
  "effectiveFrom": "2025-08-04T09:00:00Z",
  "details": {
    "benchmark": {
      "type": "fdc3.instrument",
      "id": { "CUSIP": "9128283H1" }
    },
    "offset": 0.5,
    "offsetType": "Yield" // Price, Yield
  }
}
```

---

### Custom FDC3 Intents

These are the "verbs" that trigger actions between your applications.

| Intent Name        | Description                                                                                                                               | Expected Context                     |
| :----------------- | :---------------------------------------------------------------------------------------------------------------------------------------- | :----------------------------------- |
| **`ViewPrice`**    | Raised to view the pricing details for an instrument. The **Pricing** app will listen for this.                                           | `fdc3.instrument` or `toms.position` |
| **`ViewOrder`**    | Raised to view the full details of an order. The **Ticket** app will listen for this.                                                     | `toms.order`                         |
| **`RequestPrice`** | Raised by a salesperson to send a new order to the trading desk for pricing. The **Workspace** will listen for this.                      | `toms.order`                         |
| **`CounterPrice`** | Raised by a trader to send a price quote back to the salesperson. The salesperson's **Ticket** app will listen for this.                  | `toms.order`                         |
| **`AcceptOrder`**  | Raised by a salesperson to confirm a trade after client agreement. The trader's **Workspace** will listen for this to finalize the trade. | `toms.order`                         |
| **`RejectOrder`**  | Raised by a trader to reject an order. The salesperson's **Ticket** app will listen for this.                                             | `toms.order`                         |

---

### FDC3 Workflows in Action workflows

Here’s how these contexts and intents implement the user stories.

#### Workflow 1: Trader Views Pricing Rule for a Position

This workflow links the **Workspace** and **Pricing** applications, relating to **Use Cases 3.2 and 2.1**.

1.  **Action:** Tom, the Trader, is looking at his positions in the **Workspace**. He wants to check the current pricing rule for a specific bond. He right-clicks on a row in his positions grid.
2.  **FDC3 Interaction:**
    - The **Workspace** app creates a `toms.position` context from the selected row's data.
    - The **Workspace** app raises the intent `ViewPrice` with this context:
      ```javascript
      const positionContext = {
        /* ... toms.position object ... */
      };
      fdc3.raiseIntent("ViewPrice", positionContext);
      ```
3.  **Result:**
    - The FDC3 Desktop Agent offers the user a choice of apps that can handle the `ViewPrice` intent (in this case, the **Pricing** app).
    - The user selects the **Pricing** app.
    - The **Pricing** app receives the `toms.position` context, extracts the instrument identifier (`CUSIP`), and automatically loads and displays the active pricing rule for that bond.

#### Workflow 2: Trader Opens an Order from the Workspace

This workflow links the **Workspace** and **Ticket** applications, relating to **Use Cases 1.2 and 3.2**.

1.  **Action:** A new order has arrived and appears in Tom's "Incoming Orders" blotter in his **Workspace**. He wants to view the full order details to price it. He clicks on the order summary.
2.  **FDC3 Interaction:**
    - The **Workspace** app has already received the full `toms.order` context via the `RequestPrice` intent (see next workflow). It has this context associated with the row in the blotter.
    - When Tom clicks the row, the **Workspace** raises the `ViewOrder` intent with the order's context:
      ```javascript
      const orderContext = {
        /* ... toms.order object from incoming order ... */
      };
      fdc3.raiseIntent("ViewOrder", orderContext);
      ```
3.  **Result:**
    - The FDC3 Desktop Agent resolves the intent to the **Ticket** application.
    - If the **Ticket** app is not running, it is launched.
    - The **Ticket** app is populated with all the details from the `toms.order` context, ready for Tom to analyze and price.

#### Workflow 3: The Complete Order Negotiation Lifecycle 🔄

This is the most critical workflow, involving the **Salesperson's Ticket**, the **Trader's Workspace**, and the **Trader's Ticket**. It covers **Use Cases 1.1 and 1.2**.

1.  **Salesperson Requests Price:**

    - **Action:** Sarah (Salesperson) fills out an order on her **Ticket** app and clicks "Request Price".
    - **FDC3:** Her **Ticket** app creates a `toms.order` context with the status `PendingPrice` and raises the `RequestPrice` intent. This is a targeted intent for the trader's **Workspace**.

2.  **Trader Receives Request:**

    - **Action:** The **Trader's Workspace**, listening for the `RequestPrice` intent, receives the `toms.order` context. A new line item appears in Tom's "Incoming Orders" blotter.
    - **FDC3:** No FDC3 message is sent at this step; the app simply handles the received intent.

3.  **Trader Prices the Order:**

    - **Action:** Tom opens the order in his **Ticket** app (as described in Workflow 2), enters a price, and clicks "Send Price".
    - **FDC3:** His **Ticket** app updates the received `toms.order` context with the new price and changes the status to `Priced`. It then raises the `CounterPrice` intent, targeted back at Sarah's **Ticket** instance.

4.  **Salesperson Receives Price:**

    - **Action:** Sarah's **Ticket** app, which is listening for the `CounterPrice` intent, receives the updated `toms.order` context. The price field on her screen populates, and the status changes to "Priced". She confirms with her client.

5.  **Salesperson Confirms Trade:**

    - **Action:** The client agrees. Sarah clicks "Confirm" on her **Ticket**.
    - **FDC3:** Her **Ticket** app updates the context's status to `Confirmed` and raises the `AcceptOrder` intent.

6.  **Trader's Workspace Updates:**

    - **Action:** Tom's **Workspace**, listening for the `AcceptOrder` intent, receives the final confirmed order.
    - **Result:** The order is removed from the "Incoming Orders" blotter, a new entry is added to the "Trades" blotter, and the relevant position in the "Positions" blotter is updated in real-time. The workflow is complete. ✔️
