var _createClass = function () { function defineProperties(target, props) { for (var i = 0; i < props.length; i++) { var descriptor = props[i]; descriptor.enumerable = descriptor.enumerable || false; descriptor.configurable = true; if ("value" in descriptor) descriptor.writable = true; Object.defineProperty(target, descriptor.key, descriptor); } } return function (Constructor, protoProps, staticProps) { if (protoProps) defineProperties(Constructor.prototype, protoProps); if (staticProps) defineProperties(Constructor, staticProps); return Constructor; }; }();

function _classCallCheck(instance, Constructor) { if (!(instance instanceof Constructor)) { throw new TypeError("Cannot call a class as a function"); } }

function _possibleConstructorReturn(self, call) { if (!self) { throw new ReferenceError("this hasn't been initialised - super() hasn't been called"); } return call && (typeof call === "object" || typeof call === "function") ? call : self; }

function _inherits(subClass, superClass) { if (typeof superClass !== "function" && superClass !== null) { throw new TypeError("Super expression must either be null or a function, not " + typeof superClass); } subClass.prototype = Object.create(superClass && superClass.prototype, { constructor: { value: subClass, enumerable: false, writable: true, configurable: true } }); if (superClass) Object.setPrototypeOf ? Object.setPrototypeOf(subClass, superClass) : subClass.__proto__ = superClass; }

var Alergens = function (_React$Component) {
    _inherits(Alergens, _React$Component);

    function Alergens(props) {
        _classCallCheck(this, Alergens);

        var _this = _possibleConstructorReturn(this, (Alergens.__proto__ || Object.getPrototypeOf(Alergens)).call(this, props));

        _this.state = { allergens: props.data };
        return _this;
    }

    _createClass(Alergens, [{
        key: 'get_print_codes',
        value: function get_print_codes(list) {
            var print_codes = [];
            list.forEach(function (allergen) {
                print_codes.push(allergen[0]);
            });
            if (print_codes.length == 0) {
                return 'Žiadne alergény';
            }
            return 'Alergény: ' + print_codes.join(', ');
        }
    }, {
        key: 'render',
        value: function render() {
            return React.createElement(
                'div',
                null,
                React.createElement(
                    'p',
                    { className: 'text-end m-0 p-1' },
                    this.get_print_codes(this.state.allergens)
                )
            );
        }
    }]);

    return Alergens;
}(React.Component);

export default Alergens;