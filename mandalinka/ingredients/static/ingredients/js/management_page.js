var _slicedToArray = function () { function sliceIterator(arr, i) { var _arr = []; var _n = true; var _d = false; var _e = undefined; try { for (var _i = arr[Symbol.iterator](), _s; !(_n = (_s = _i.next()).done); _n = true) { _arr.push(_s.value); if (i && _arr.length === i) break; } } catch (err) { _d = true; _e = err; } finally { try { if (!_n && _i["return"]) _i["return"](); } finally { if (_d) throw _e; } } return _arr; } return function (arr, i) { if (Array.isArray(arr)) { return arr; } else if (Symbol.iterator in Object(arr)) { return sliceIterator(arr, i); } else { throw new TypeError("Invalid attempt to destructure non-iterable instance"); } }; }();

var _createClass = function () { function defineProperties(target, props) { for (var i = 0; i < props.length; i++) { var descriptor = props[i]; descriptor.enumerable = descriptor.enumerable || false; descriptor.configurable = true; if ("value" in descriptor) descriptor.writable = true; Object.defineProperty(target, descriptor.key, descriptor); } } return function (Constructor, protoProps, staticProps) { if (protoProps) defineProperties(Constructor.prototype, protoProps); if (staticProps) defineProperties(Constructor, staticProps); return Constructor; }; }();

function _classCallCheck(instance, Constructor) { if (!(instance instanceof Constructor)) { throw new TypeError("Cannot call a class as a function"); } }

function _possibleConstructorReturn(self, call) { if (!self) { throw new ReferenceError("this hasn't been initialised - super() hasn't been called"); } return call && (typeof call === "object" || typeof call === "function") ? call : self; }

function _inherits(subClass, superClass) { if (typeof superClass !== "function" && superClass !== null) { throw new TypeError("Super expression must either be null or a function, not " + typeof superClass); } subClass.prototype = Object.create(superClass && superClass.prototype, { constructor: { value: subClass, enumerable: false, writable: true, configurable: true } }); if (superClass) Object.setPrototypeOf ? Object.setPrototypeOf(subClass, superClass) : subClass.__proto__ = superClass; }

import { useState } from "react";
import IngredientWidget from "./ingredient_widget.js";
import getCookie from "./get_cookie.js";

function SearchBar(props) {
  return React.createElement(
    "div",
    null,
    React.createElement(
      "div",
      { className: "row search justify-content-center" },
      React.createElement(
        "div",
        { className: "col-auto search__container" },
        React.createElement(
          "form",
          { onSubmit: props.handleSubmit, method: "post" },
          React.createElement("input", {
            name: "search_text",
            type: "text",
            className: "search__input",
            maxLength: "32",
            placeholder: "Hladaj ingredienciu"
          }),
          React.createElement("button", { type: "submit", hidden: true })
        )
      )
    )
  );
}

var IngredientManagementPage = function (_React$Component) {
  _inherits(IngredientManagementPage, _React$Component);

  function IngredientManagementPage(props) {
    _classCallCheck(this, IngredientManagementPage);

    var _this = _possibleConstructorReturn(this, (IngredientManagementPage.__proto__ || Object.getPrototypeOf(IngredientManagementPage)).call(this, props));

    _initialiseProps.call(_this);

    var _useImmer = useImmer({}),
        _useImmer2 = _slicedToArray(_useImmer, 2),
        ingredients = _useImmer2[0],
        setIngredients = _useImmer2[1];

    var _useState = useState(false),
        _useState2 = _slicedToArray(_useState, 2),
        error = _useState2[0],
        setError = _useState2[1];

    return _this;
  }

  _createClass(IngredientManagementPage, [{
    key: "componentDidMount",
    value: function componentDidMount() {
      this.load_ingredients("");
    }
  }, {
    key: "render",
    value: function render() {
      console.log("Rendering: ", ingredients);
      return React.createElement(
        "div",
        null,
        React.createElement(SearchBar, { handleSubmit: this.handleSearch, error: this.state.error }),
        ingredients.map(function (ingredient) {
          React.createElement(IngredientWidget, { key: ingredient.id, ingredient: ingredient });
        })
      );
    }
  }]);

  return IngredientManagementPage;
}(React.Component);

var _initialiseProps = function _initialiseProps() {
  var _this2 = this;

  this.handleSearch = function (event) {
    event.preventDefault();
    var formdata = new FormData(event.target);

    _this2.load_ingredients(formdata.get("search_text"));
  };

  this.load_ingredients = function (search_text) {
    console.log("fetching", search_text);
    fetch("/ingredients/api/search/?q=" + search_text, {
      method: "GET",
      mode: "same-origin",
      headers: {
        "Content-Type": "application/json",
        "X-CSRFToken": getCookie("csrftoken")
      }
    }).then(function (response) {
      return response.json();
    }).then(function (response) {
      console.log(response);
      _this2.setIngredients(response);
    }).catch(function (error) {
      console.log("Couldnt fetch: ", error);
      _this2.setIngredients([]);
    });
  };
};

export default IngredientManagementPage;