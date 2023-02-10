function JsxAttribute(props) {
  const className =
    "attr btn btn-outline-primary " +
    (props.selected ? "selected " : "") +
    (props.favorite ? "favorite " : "") +
    (props.type != undefined ? props.type : "");

  return (
    <a
      className={className}
      role="button"
      aria-disabled="true"
      key={props.title}
    >
      {props.title}
    </a>
  );
}

export default class Attributes extends React.Component {
  render() {
    const attr_type = (
      <JsxAttribute
        title={this.props.type}
        selected={false}
        favorite={false}
        type={this.props.type}
      />
    );

    const attrs_fav_sel = [];
    const attrs_sel = [];
    const attrs_fav = [];
    const attrs_rest = [];

    for (const [key, value] of Object.entries(this.props.attrs)) {
      if (value.favorite && value.selected) {
        attrs_fav_sel.push(
          <JsxAttribute
            title={key}
            selected={value.selected}
            favorite={value.favorite}
            key={key}
          />
        );
      } else if (value.selected) {
        attrs_sel.push(
          <JsxAttribute
            title={key}
            selected={value.selected}
            favorite={value.favorite}
            key={key}
          />
        );
      } else if (value.favorite) {
        attrs_fav.push(
          <JsxAttribute
            title={key}
            selected={value.selected}
            favorite={value.favorite}
            key={key}
          />
        );
      } else {
        attrs_rest.push(
          <JsxAttribute
            title={key}
            selected={value.selected}
            favorite={value.favorite}
            key={key}
          />
        );
      }
    }

    return (
      <div className="attributes d-flex justify-content-center flex-wrap">
        {attr_type}
        {attrs_fav_sel}
        {attrs_sel}
        {attrs_fav}
        {attrs_rest}
      </div>
    );
  }
}
