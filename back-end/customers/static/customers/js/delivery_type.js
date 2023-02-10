export default function DeliveryType(props) {
  var pickup = void 0,
    delivery = void 0;
  if (props.pickup) {
    pickup = React.createElement(
      "a",
      { className: "active" },
      React.createElement(
        "span",
        { className: "material-symbols-rounded md-36 fill" },
        "pedal_bike"
      )
    );
    delivery = React.createElement(
      "a",
      { href: "#", onClick: props.toggle, className: "inactive" },
      React.createElement(
        "span",
        { className: "material-symbols-rounded md-36" },
        "storefront"
      )
    );
  } else {
    pickup = React.createElement(
      "a",
      { href: "#", onClick: props.toggle, className: "inactive" },
      React.createElement(
        "span",
        { className: "material-symbols-rounded md-36" },
        "pedal_bike"
      )
    );
    delivery = React.createElement(
      "a",
      { className: "active" },
      React.createElement(
        "span",
        { className: "material-symbols-rounded md-36 fill" },
        "storefront"
      )
    );
  }
  return React.createElement(
    "div",
    { className: "delivery-type hstack" },
    pickup,
    React.createElement("div", { className: "vr" }),
    delivery
  );
}
