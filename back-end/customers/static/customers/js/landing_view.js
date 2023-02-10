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

var root_div = document.getElementById("Account");
var root = ReactDOM.createRoot(root_div);

var AccountIcon = (function (_React$PureComponent) {
  _inherits(AccountIcon, _React$PureComponent);

  function AccountIcon(props) {
    _classCallCheck(this, AccountIcon);

    var _this = _possibleConstructorReturn(
      this,
      (AccountIcon.__proto__ || Object.getPrototypeOf(AccountIcon)).call(
        this,
        props
      )
    );

    _this.state = {
      isHovering: false,
      isAuthenticated: root_div.getAttribute("is_authenticated"),
    };
    _this.myAccountLink = root_div.getAttribute("my_account_link");
    _this.logOutLink = root_div.getAttribute("log_out_link");
    _this.newUserLink = root_div.getAttribute("new_user_link");
    _this.handleMouseOver = _this.handleMouseOver.bind(_this);
    _this.handleMouseOut = _this.handleMouseOut.bind(_this);
    return _this;
  }

  _createClass(AccountIcon, [
    {
      key: "handleMouseOver",
      value: function handleMouseOver(e) {
        this.setState({ isHovering: true });
      },
    },
    {
      key: "handleMouseOut",
      value: function handleMouseOut(e) {
        this.setState({ isHovering: false });
      },
    },
    {
      key: "render",
      value: function render() {
        if (this.state.isAuthenticated === "True") {
          return React.createElement(
            "div",
            {
              id: "AccountIcons",
              className: "position-absolute top-0 end-0",
              onMouseOver: this.handleMouseOver,
              onMouseOut: this.handleMouseOut,
            },
            this.state.isHovering
              ? React.createElement(
                  "div",
                  { className: "btn-group-vertical" },
                  React.createElement(
                    "a",
                    null,
                    React.createElement(
                      "span",
                      {
                        id: "Person",
                        className: "material-symbols-rounded menu",
                      },
                      "person"
                    )
                  ),
                  React.createElement(
                    "a",
                    { href: this.myAccountLink },
                    React.createElement(
                      "span",
                      {
                        id: "ManageAccount",
                        className: "material-symbols-rounded option",
                      },
                      "manage_accounts"
                    ),
                    React.createElement(
                      "span",
                      { className: "custom-tooltip" },
                      "Upravte si profil"
                    )
                  ),
                  React.createElement(
                    "a",
                    { href: this.logOutLink },
                    React.createElement(
                      "span",
                      {
                        id: "LogOut",
                        className: "material-symbols-rounded option",
                      },
                      "logout"
                    ),
                    React.createElement(
                      "span",
                      { className: "custom-tooltip" },
                      "Odhl\xE1ste sa"
                    )
                  )
                )
              : React.createElement(
                  "div",
                  { className: "btn-group-vertical" },
                  React.createElement(
                    "a",
                    null,
                    React.createElement(
                      "span",
                      {
                        id: "Person",
                        className: "material-symbols-rounded menu",
                      },
                      "person"
                    )
                  )
                )
          );
        } else {
          return React.createElement(
            "div",
            {
              id: "AccountIcons",
              className: "position-absolute top-0 end-0",
              onMouseOver: this.handleMouseOver,
              onMouseOut: this.handleMouseOut,
            },
            this.state.isHovering
              ? React.createElement(
                  "div",
                  { className: "btn-group-vertical" },
                  React.createElement(
                    "a",
                    null,
                    React.createElement(
                      "span",
                      {
                        id: "Person",
                        className: "material-symbols-rounded menu",
                      },
                      "person"
                    )
                  ),
                  React.createElement(
                    "a",
                    {
                      href: "#",
                      "data-bs-toggle": "modal",
                      "data-bs-target": "#LoginModal",
                    },
                    React.createElement(
                      "span",
                      {
                        id: "LoginModalButton",
                        className: "material-symbols-rounded option",
                      },
                      "login"
                    ),
                    React.createElement(
                      "span",
                      { className: "custom-tooltip" },
                      "Prihl\xE1ste sa"
                    )
                  ),
                  React.createElement(
                    "a",
                    { href: this.newUserLink },
                    React.createElement(
                      "span",
                      {
                        id: "SignUp",
                        className: "material-symbols-rounded option",
                      },
                      "person_add"
                    ),
                    React.createElement(
                      "span",
                      { className: "custom-tooltip" },
                      "Vytvorte si \xFA\u010Det"
                    )
                  )
                )
              : React.createElement(
                  "div",
                  { className: "btn-group-vertical" },
                  React.createElement(
                    "a",
                    null,
                    React.createElement(
                      "span",
                      {
                        id: "Person",
                        className: "material-symbols-rounded menu",
                      },
                      "person"
                    )
                  )
                )
          );
        }
      },
    },
  ]);

  return AccountIcon;
})(React.PureComponent);

root.render(React.createElement(AccountIcon, null));
