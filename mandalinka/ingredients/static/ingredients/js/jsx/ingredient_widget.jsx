export default class IngredientWidget extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      ingredient: props.ingredient,
    }
  }
  
  render() {
    return (
      <div id="ingredients-result">
        <p className={"ingredient-button "+this.state.ingredient.status}>
          {this.state.ingredient}
        </p>
      </div>
    )
  }
}