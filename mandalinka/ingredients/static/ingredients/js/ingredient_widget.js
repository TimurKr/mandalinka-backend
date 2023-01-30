var _createClass = function () { function defineProperties(target, props) { for (var i = 0; i < props.length; i++) { var descriptor = props[i]; descriptor.enumerable = descriptor.enumerable || false; descriptor.configurable = true; if ("value" in descriptor) descriptor.writable = true; Object.defineProperty(target, descriptor.key, descriptor); } } return function (Constructor, protoProps, staticProps) { if (protoProps) defineProperties(Constructor.prototype, protoProps); if (staticProps) defineProperties(Constructor, staticProps); return Constructor; }; }();

function _classCallCheck(instance, Constructor) { if (!(instance instanceof Constructor)) { throw new TypeError("Cannot call a class as a function"); } }

function _possibleConstructorReturn(self, call) { if (!self) { throw new ReferenceError("this hasn't been initialised - super() hasn't been called"); } return call && (typeof call === "object" || typeof call === "function") ? call : self; }

function _inherits(subClass, superClass) { if (typeof superClass !== "function" && superClass !== null) { throw new TypeError("Super expression must either be null or a function, not " + typeof superClass); } subClass.prototype = Object.create(superClass && superClass.prototype, { constructor: { value: subClass, enumerable: false, writable: true, configurable: true } }); if (superClass) Object.setPrototypeOf ? Object.setPrototypeOf(subClass, superClass) : subClass.__proto__ = superClass; }

var IngredientWidget = function (_React$Component) {
  _inherits(IngredientWidget, _React$Component);

  function IngredientWidget(props) {
    _classCallCheck(this, IngredientWidget);

    var _this = _possibleConstructorReturn(this, (IngredientWidget.__proto__ || Object.getPrototypeOf(IngredientWidget)).call(this, props));

    _this.state = {
      ingredient: props.ingredient
    };
    return _this;
  }

  _createClass(IngredientWidget, [{
    key: "render",
    value: function render() {
      return React.createElement(
        "div",
        { id: "ingredients-result" },
        React.createElement(
          "p",
          { className: "ingredient-button " + this.state.ingredient.status },
          this.state.ingredient
        )
      );
    }
  }]);

  return IngredientWidget;
}(React.Component);

export default IngredientWidget;