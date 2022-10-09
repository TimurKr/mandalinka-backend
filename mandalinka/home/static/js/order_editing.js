var _createClass = function () { function defineProperties(target, props) { for (var i = 0; i < props.length; i++) { var descriptor = props[i]; descriptor.enumerable = descriptor.enumerable || false; descriptor.configurable = true; if ("value" in descriptor) descriptor.writable = true; Object.defineProperty(target, descriptor.key, descriptor); } } return function (Constructor, protoProps, staticProps) { if (protoProps) defineProperties(Constructor.prototype, protoProps); if (staticProps) defineProperties(Constructor, staticProps); return Constructor; }; }();

function _classCallCheck(instance, Constructor) { if (!(instance instanceof Constructor)) { throw new TypeError("Cannot call a class as a function"); } }

function _possibleConstructorReturn(self, call) { if (!self) { throw new ReferenceError("this hasn't been initialised - super() hasn't been called"); } return call && (typeof call === "object" || typeof call === "function") ? call : self; }

function _inherits(subClass, superClass) { if (typeof superClass !== "function" && superClass !== null) { throw new TypeError("Super expression must either be null or a function, not " + typeof superClass); } subClass.prototype = Object.create(superClass && superClass.prototype, { constructor: { value: subClass, enumerable: false, writable: true, configurable: true } }); if (superClass) Object.setPrototypeOf ? Object.setPrototypeOf(subClass, superClass) : subClass.__proto__ = superClass; }

var root = ReactDOM.createRoot(document.getElementById('CurrentOrder'));

import RecipeWidget from './recipe_widget.js';
import DeliveryType from './delivery_type.js';
import getCookie from './get_cookie.js';
import Cart from './cart.js';

var OrderEditing = function (_React$Component) {
    _inherits(OrderEditing, _React$Component);

    function OrderEditing(props) {
        _classCallCheck(this, OrderEditing);

        var _this = _possibleConstructorReturn(this, (OrderEditing.__proto__ || Object.getPrototypeOf(OrderEditing)).call(this, props));

        _this.toggle_pickup = function () {
            var put_info = {
                method: 'PUT',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': getCookie('csrftoken')
                },
                body: JSON.stringify({
                    order_id: _this.state.order_id
                }),
                mode: 'same-origin'
            };

            fetch('/toggle_pickup', put_info).then(function (response) {
                return response.json();
            }).then(function (response) {
                _this.setState({ pickup: response.pickup });
            });
        };

        _this.state = {
            date: '...',
            recipes: [],
            thumbnail: '',
            order_id: undefined,
            price: "66.66"
        };
        return _this;
    }

    _createClass(OrderEditing, [{
        key: 'componentDidMount',
        value: function componentDidMount() {
            var _this2 = this;

            fetch('/recepty/load_next_order').then(function (response) {
                return response.json();
            }).then(function (response) {
                _this2.setState({
                    date: response.date,
                    pickup: response.pickup,
                    recipes: response.recipes,
                    order_id: response.order_id,
                    price: response.price
                });
            }).catch(function (error) {
                console.log("Chybyčka: ", error);
            });
        }
    }, {
        key: 'render',
        value: function render() {

            var recipes = [];
            for (var i = 0; i < this.state.recipes.length; i++) {
                recipes.push(React.createElement(RecipeWidget, {
                    key: i,
                    thumbnail: this.state.recipes[i].thumbnail,
                    title: this.state.recipes[i].title,
                    description: this.state.recipes[i].description,
                    type: this.state.recipes[i].type,
                    attributes: this.state.recipes[i].attributes,
                    alergens: this.state.recipes[i].alergens,
                    order_data: this.state.recipes[i].order_data,
                    price: this.state.recipes[i].price
                }));
            }

            return React.createElement(
                'div',
                { className: 'order-editing container-fluid position-relative' },
                React.createElement(
                    'div',
                    { className: 'header d-flex align-items-center mb-3' },
                    React.createElement(
                        'div',
                        { className: 'me-auto p-2' },
                        React.createElement(
                            'h2',
                            null,
                            'Recepty na podelok ',
                            this.state.date
                        )
                    ),
                    React.createElement(DeliveryType, { pickup: this.state.pickup, toggle: this.toggle_pickup }),
                    React.createElement(Cart, { price: this.state.price })
                ),
                React.createElement(
                    'div',
                    { className: 'row gx-3 gy-4' },
                    recipes
                )
            );
        }
    }]);

    return OrderEditing;
}(React.Component);

root.render(React.createElement(OrderEditing, null));