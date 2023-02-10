export default function price_tag(props) {
  return React.createElement(
    "p",
    null,
    Math.floor(props.price),
    React.createElement("sup", null, Math.round(100 * (props.price % 1))),
    "\u20AC",
    props.children
  );
}
