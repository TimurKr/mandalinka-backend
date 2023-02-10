export default function price_tag(props) {
  return (
    <p>
      {Math.floor(props.price)}
      <sup>{Math.round(100 * (props.price % 1))}</sup>€{props.children}
    </p>
  );
}
