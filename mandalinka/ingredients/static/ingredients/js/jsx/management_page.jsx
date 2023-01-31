import { useImmer } from "use-immer";

import IngredientWidget from "./ingredient_widget.js";
import getCookie from "./get_cookie.js";

function SearchBar(props) {
  return (
    <div>
      <div className="row search justify-content-center">
        <div className="col-auto search__container">
          <form onSubmit={props.handleSubmit} method="post">
            <input
              name="search_text"
              type="text"
              className="search__input"
              maxLength="32"
              placeholder="Hladaj ingredienciu"
            ></input>
            <button type="submit" hidden></button>
          </form>
        </div>
      </div>
    </div>
  );
}

export default class IngredientManagementPage extends React.Component {
  constructor(props) {
    super(props);

    const [ingredients, setIngredients] = useImmer({});
    const [error, setError] = React.useState(false);
  }

  componentDidMount() {
    this.load_ingredients("");
  }

  handleSearch = (event) => {
    event.preventDefault();
    const formdata = new FormData(event.target);

    this.load_ingredients(formdata.get("search_text"));
  };

  load_ingredients = (search_text) => {
    console.log("fetching", search_text);
    fetch(`/ingredients/api/search/?q=${search_text}`, {
      method: "GET",
      mode: "same-origin",
      headers: {
        "Content-Type": "application/json",
        "X-CSRFToken": getCookie("csrftoken"),
      },
    })
      .then((response) => response.json())
      .then((response) => {
        console.log(response);
        this.setIngredients(response);
      })
      .catch((error) => {
        console.log("Couldnt fetch: ", error);
        this.setIngredients([]);
      });
  };

  render() {
    console.log("Rendering: ", ingredients);
    return (
      <div>
        <SearchBar handleSubmit={this.handleSearch} error={this.state.error} />
        {ingredients.map((ingredient) => {
          <IngredientWidget key={ingredient.id} ingredient={ingredient} />;
        })}
      </div>
    );
  }
}
