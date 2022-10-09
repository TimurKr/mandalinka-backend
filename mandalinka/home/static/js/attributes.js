var _createClass = function () { function defineProperties(target, props) { for (var i = 0; i < props.length; i++) { var descriptor = props[i]; descriptor.enumerable = descriptor.enumerable || false; descriptor.configurable = true; if ("value" in descriptor) descriptor.writable = true; Object.defineProperty(target, descriptor.key, descriptor); } } return function (Constructor, protoProps, staticProps) { if (protoProps) defineProperties(Constructor.prototype, protoProps); if (staticProps) defineProperties(Constructor, staticProps); return Constructor; }; }();

function _classCallCheck(instance, Constructor) { if (!(instance instanceof Constructor)) { throw new TypeError("Cannot call a class as a function"); } }

function _possibleConstructorReturn(self, call) { if (!self) { throw new ReferenceError("this hasn't been initialised - super() hasn't been called"); } return call && (typeof call === "object" || typeof call === "function") ? call : self; }

function _inherits(subClass, superClass) { if (typeof superClass !== "function" && superClass !== null) { throw new TypeError("Super expression must either be null or a function, not " + typeof superClass); } subClass.prototype = Object.create(superClass && superClass.prototype, { constructor: { value: subClass, enumerable: false, writable: true, configurable: true } }); if (superClass) Object.setPrototypeOf ? Object.setPrototypeOf(subClass, superClass) : subClass.__proto__ = superClass; }

var Attributes = function (_React$Component) {
    _inherits(Attributes, _React$Component);

    function Attributes() {
        _classCallCheck(this, Attributes);

        return _possibleConstructorReturn(this, (Attributes.__proto__ || Object.getPrototypeOf(Attributes)).apply(this, arguments));
    }

    _createClass(Attributes, [{
        key: "render",
        value: function render() {
            var attrs = [];
            this.props.attrs.forEach(function (attr) {
                attrs.push(React.createElement(
                    "a",
                    { className: "attr btn btn-outline-primary", role: "button", "aria-disabled": "true", key: attr },
                    attr
                ));
            });
            return React.createElement(
                "div",
                { className: "attributes d-flex flex-wrap justify-content-center" },
                attrs
            );
        }
    }]);

    return Attributes;
}(React.Component);

export default Attributes;