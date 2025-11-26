---
description: This section contains reference documentation for the ROW_NUMBER function.
---

# ROW\_NUMBER

Assigns a row number to all the rows in a specified table.

## Signature

> ROW\_NUMBER()

## ROW\_NUMBER examples

* [Order transactions by payment date](round-1-1.md#order-transactions-by-payment-date)
* [Identify the top two transactions by customer, ordered by transaction amount](round-1-1.md#identify-the-top-two-transactions-by-customer-ordered-by-transaction-amount)
* [Identify customers with the highest number of transactions](round-1-1.md#identify-customers-with-the-highest-number-of-transactions)

### Order transactions by payment date

Order transactions by the payment date and assign them row numbers.

{% code overflow="wrap" %}
```sql
select customer_id, payment_date, amount, ROW_NUMBER() OVER(ORDER BY payment_date from payment;

```
{% endcode %}

<table><thead><tr><th>customer_id</th><th>payment_date</th><th>amount</th><th data-type="number">row_number</th></tr></thead><tbody><tr><td>416</td><td>2023-02-14 21:21:59.996577</td><td>2.99</td><td>1</td></tr><tr><td>516</td><td>2023-02-14 21:23:39.996577</td><td>4.99</td><td>2</td></tr><tr><td>239</td><td>2023-02-14 21:29:00.996577</td><td>4.99</td><td>3</td></tr><tr><td>592</td><td>2023-02-14 21:41:12.996577</td><td>6.99</td><td>4</td></tr><tr><td>49</td><td>2023-02-14 21:44:52.996577</td><td>0.99</td><td>5</td></tr><tr><td>264</td><td>2023-02-14 21:44:53.996577</td><td>3.99</td><td>6</td></tr><tr><td>46</td><td>2023-02-14 21:45:29.996577</td><td>4.99</td><td>7</td></tr><tr><td>481</td><td>2023-02-14 22:03:35.996577</td><td>2.99</td><td>8</td></tr><tr><td>139</td><td>2023-02-14 22:11:22.996577</td><td>2.99</td><td>9</td></tr><tr><td>595</td><td>2023-02-14 22:16:01.996577</td><td>2.99</td><td>10</td></tr></tbody></table>

### Identify the top two transactions by customer, ordered by transaction amount

{% code overflow="wrap" %}
```sql
WITH payment_cte as (SELECT ROW_NUMBER() OVER(PARTITION BY customer_id ORDER BY amount DESC), customer_id, payment_date, amount from payment) SELECT row_number, customer_id, payment_date, amount from payment_cte WHERE row_number <= 2;
```
{% endcode %}

<table><thead><tr><th>row_number</th><th>customer_id</th><th>payment_date</th><th data-type="number">amount</th></tr></thead><tbody><tr><td>1</td><td>1</td><td>2023-02-15 19:37:12.996577</td><td>9.99</td></tr><tr><td>2</td><td>1</td><td>2023-04-11 08:42:12.996577</td><td>7.99</td></tr><tr><td>1</td><td>2</td><td>2023-04-30 12:16:09.996577</td><td>10.99</td></tr><tr><td>2</td><td>2</td><td>2023-04-30 14:49:39.996577</td><td>8.99</td></tr><tr><td>1</td><td>3</td><td>2023-04-27 18:51:38.996577</td><td>8.99</td></tr><tr><td>2</td><td>3</td><td>2023-03-21 19:19:14.996577</td><td>10.99</td></tr><tr><td>1</td><td>4</td><td>2023-03-18 03:43:10.996577</td><td>10.99</td></tr><tr><td>2</td><td>4</td><td>2023-03-20 11:24:06.996577</td><td>10.99</td></tr></tbody></table>

### Identify customers with the highest number of transactions

Find the number of transactions ranked for each customer. The customer with the highest number of transactions will have a rank of 1, and so on. Order records by the total transactions in descending order. In your rankings, return a unique rank value (to cover multiple customers with the same number of transactions).

{% code overflow="wrap" %}
```sql
SELECT customer_id, count(*), ROW_NUMBER() OVER(ORDER BY count(*) DESC, customer_id ASC) from payment GROUP BY customer_id;
```
{% endcode %}

| customer\_id | count | row\_number |
| ------------ | ----- | ----------- |
| 148          | 45    | 1           |
| 245          | 42    | 2           |
| 144          | 39    | 3           |
| 253          | 39    | 4           |
| 410          | 36    | 5           |
| 368          | 34    | 6           |

\
\\
