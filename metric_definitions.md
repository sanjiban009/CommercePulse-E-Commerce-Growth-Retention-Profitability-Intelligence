# CommercePulse — Metric Definitions

**Snapshot:** through October 2026. **Calendar convention:** Indian financial year April–March. **Currency:** Indian rupees (INR), displayed as ₹, lakh (L) or crore (Cr). **Source grain:** month × category × region × order source × customer order type × payment method.

| Measure | Calculation | Caution |
|---|---|---|
| Gross placed order value | Sum of modeled pre-discount orders | Not realized sales |
| Discount value | Sum of promotional markdown | Deduct before cancellation/returns |
| Net realized revenue | Gross value − discounts − canceled value − refunded return value | Excludes tax modeling |
| Contribution profit | Net revenue − COGS − forward/reverse freight − payment fees − allocated marketing | Excludes corporate/fixed overhead and taxes |
| Contribution margin | Contribution / net realized revenue | Positive margin is not net profit |
| Conversion | Placed orders / modeled sessions | Visits are generated, not web-analytics events |
| Average order value | Net realized revenue / placed orders | After all value leakage by design |
| Return rate | Returned orders / shipped orders | Canceled orders not in denominator |
| Cancellation rate | Canceled orders / placed orders | Pre-dispatch cancellations only |
| COD share | COD placed orders / all placed orders | Both New/Returning classified |
| On-time rate | (Shipped orders − late shipped orders) / shipped orders | Simplified SLA proxy |
| Average delivery days | Sum(weighted transit days) / shipped orders | Weighted by modeled shipped orders |
| Logistics cost per shipment | Forward + reverse freight / shipped orders | No warehouse fixed costs |
| Returning order share | Returning-type orders / all placed orders | **Not customer retention**; no unique IDs |
| Marketing per new order | All allocated marketing / New-type orders | Proxy, not incremental CAC |
| Revenue / marketing | Net realized revenue / marketing spend | Allocation ratio, not attributed/causal ROAS |
| Outlook | Actual current FYTD + prior-year remainder × capped current FYTD growth factor × 0.9 growth retention | Heuristic; not a statistical forecast |

## Reporting windows

- When `MATCHED FYTD` is **on**, every year uses **April through October** (7 months), including FY2024–25 and FY2025–26. This produces a comparable time span for FY2026–27.
- When it is **off**, past complete financial years show April–March (12 months); FY2026–27 remains actual April–October (7 months).
- The forecast is only supplied for **FY2026–27**, and projected months are explicitly colored violet; observed monthly values are teal.

## Reconciliation tests

For each 7,440-row record:

```text
ABS(net_revenue - (gross_order_value - discounts - cancelled_value - return_value)) < 0.011
ABS(contribution - (net_revenue - cogs - logistics_cost - payment_fees - marketing_spend)) < 0.011
```

The Excel workbook contains 1,860 monthly consolidated source rows; its totals agree with the detailed dataset up to floating-point rounding.

## Scenario sensitivity assumptions

- **Conversion uplift:** applied proportionately to the baseline FY outlook at unchanged traffic and AOV. Incremental sales bear observed variable COGS, freight and payment fees.
- **Return-rate reduction:** reduces the modeled annual refund value by the ratio of percentage-point improvement to observed shipped-order return rate; incremental recovered revenue bears variable COGS.
- **Logistics cost saving:** multiplies modeled annual freight spend by the selected saving percentage.
- Effects are additive and omit fixed overhead, taxes, elasticity, inventory capacity, customer acquisition effects and cannibalization. No causal identification is claimed.
