var _createClass = (function () {
  function defineProperties(target, props) {
    for (var i = 0; i < props.length; i++) {
      var descriptor = props[i];
      descriptor.enumerable = descriptor.enumerable || false;
      descriptor.configurable = true;
      if ("value" in descriptor) descriptor.writable = true;
      Object.defineProperty(target, descriptor.key, descriptor);
    }
  }
  return function (Constructor, protoProps, staticProps) {
    if (protoProps) defineProperties(Constructor.prototype, protoProps);
    if (staticProps) defineProperties(Constructor, staticProps);
    return Constructor;
  };
})();

function _classCallCheck(instance, Constructor) {
  if (!(instance instanceof Constructor)) {
    throw new TypeError("Cannot call a class as a function");
  }
}

function _possibleConstructorReturn(self, call) {
  if (!self) {
    throw new ReferenceError(
      "this hasn't been initialised - super() hasn't been called"
    );
  }
  return call && (typeof call === "object" || typeof call === "function")
    ? call
    : self;
}

function _inherits(subClass, superClass) {
  if (typeof superClass !== "function" && superClass !== null) {
    throw new TypeError(
      "Super expression must either be null or a function, not " +
        typeof superClass
    );
  }
  subClass.prototype = Object.create(superClass && superClass.prototype, {
    constructor: {
      value: subClass,
      enumerable: false,
      writable: true,
      configurable: true,
    },
  });
  if (superClass)
    Object.setPrototypeOf
      ? Object.setPrototypeOf(subClass, superClass)
      : (subClass.__proto__ = superClass);
}

import PriceTag from "./price_tag.js";

var Cart = (function (_React$Component) {
  _inherits(Cart, _React$Component);

  function Cart() {
    _classCallCheck(this, Cart);

    return _possibleConstructorReturn(
      this,
      (Cart.__proto__ || Object.getPrototypeOf(Cart)).apply(this, arguments)
    );
  }

  _createClass(Cart, [
    {
      key: "render",
      value: function render() {
        return React.createElement(
          "div",
          { className: "cart" },
          React.createElement(
            "a",
            {
              type: "button",
              className: "cart",
              "data-bs-toggle": "modal",
              "data-bs-target": "#exampleModal",
            },
            React.createElement(
              PriceTag,
              { price: this.props.price },
              React.createElement(
                "span",
                { className: "material-symbols-rounded" },
                "shopping_cart"
              )
            )
          ),
          React.createElement(
            "div",
            {
              className: "modal fade",
              id: "exampleModal",
              tabIndex: "-1",
              "aria-labelledby": "exampleModalLabel",
              "aria-hidden": "true",
            },
            React.createElement(
              "div",
              { className: "modal-dialog" },
              React.createElement(
                "div",
                { className: "modal-content" },
                React.createElement(
                  "div",
                  { className: "modal-header" },
                  React.createElement(
                    "h1",
                    { className: "modal-title fs-5", id: "exampleModalLabel" },
                    "Objend\xE1vka"
                  ),
                  React.createElement("button", {
                    type: "button",
                    className: "btn-close",
                    "data-bs-dismiss": "modal",
                    "aria-label": "Close",
                  })
                ),
                React.createElement(
                  "div",
                  { className: "modal-body" },
                  "Tu bude raz zoznam objedn\xE1vky"
                )
              )
            )
          )
        );
      },
    },
  ]);

  return Cart;
})(React.Component);

export default Cart;
