import { useImmer } from "use-immer";
import { useState, useEffect } from "react";
import React from "react";
import IngredientWidget from "./ingredient_widget.jsx";
import getCookie from "./get_cookie.jsx";

function SearchBar(props) {
  return (
    <div>
      <div className="row search justify-content-center">
        <div className="col-auto search__container">
          <form onSubmit={props.handleSubmit} method="post">
            {}
            <input
              name="search_text"
              type="text"
              className={"search__input " + (props.error ? "error" : "")}
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

export default function IngredientManagementPage(props) {
  const [ingredients, setIngredients] = useImmer([]);
  const [error, setError] = useState(false);

  useEffect(() => {
    load_ingredients("");
  }, []);

  function handleSearch(event) {
    event.preventDefault();
    const formdata = new FormData(event.target);
    load_ingredients(formdata.get("search_text"));
  }

  function load_ingredients(search_text) {
    console.log(props);
    fetch(props.search_url + "?q=" + search_text, {
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
        setIngredients(response);
        setError(false);
      })
      .catch((error) => {
        console.log("Couldnt fetch: ", error);
        setError(true);
        setIngredients([]);
      });
  }

  return (
    <div>
      <SearchBar handleSubmit={handleSearch} error={error} />
      {error ? (
        <div id="no-results-error">Error with server</div>
      ) : ingredients.length ? (
        <div id="ingredients-result">
          {ingredients.map((ingredient) => (
            <IngredientWidget
              key={ingredient.id}
              ingredient={ingredient}
              url={props.ingredient_url}
            />
          ))}
        </div>
      ) : (
        <div id="no-results-error">Nothing found...</div>
      )}
    </div>
  );
}
