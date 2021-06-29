select e.FirstName ||' '|| e.LastName AS employee,
e.email,
    i.invoiceid,
    i.customerid,
    i.invoicedate,
    i.billingaddress,
    i.billingcountry,
    i.billingpostalcode,
    i.total
from customers as c, invoices as i
on c.customerid = i.customerid
join employees as e on e.employeeid = c.supportrepid
order by employee ASC