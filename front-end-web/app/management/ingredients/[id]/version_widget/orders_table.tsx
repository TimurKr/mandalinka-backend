import { IngredientVersion } from "@/components/fetching/ingredient_detail";

export default function OrdersTable({ data }: { data: IngredientVersion }) {
  return (
    <>
      <table className="w-full table-auto pt-1">
        <thead className="w-full justify-between text-xs uppercase">
          <tr>
            <th scope="col" className="px-2 py-2">
              Dátum objednávky
            </th>
            <th scope="col" className="px-2 py-2">
              Dátum doručenia
            </th>
            <th scope="col" className="px-2 py-2">
              Množstvo
            </th>
            <th scope="col" className="px-2 py-2">
              Cena
            </th>
            <th scope="col" className="px-2 py-2">
              Akcie
            </th>
          </tr>
        </thead>
        <tbody>
          {data.orders.length > 0 ? (
            data.orders.map((order, index) => (
              <tr className="justify-between">
                <td>{order.order_date}</td>
                <td>{order.delivery_date}</td>
                <td>
                  {order.amount} {data.unit}
                </td>
                <td>TODO: cena</td>
                <td>
                  <a href="#">Edit</a>
                </td>
              </tr>
            ))
          ) : (
            <tr className="w-full text-center text-sm text-gray-500">
              <td colSpan={5} className="pb-2">
                Žiadne objednávky
              </td>
            </tr>
          )}
        </tbody>
      </table>
    </>
  );
}
