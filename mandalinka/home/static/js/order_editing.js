var _slicedToArray = function () { function sliceIterator(arr, i) { var _arr = []; var _n = true; var _d = false; var _e = undefined; try { for (var _i = arr[Symbol.iterator](), _s; !(_n = (_s = _i.next()).done); _n = true) { _arr.push(_s.value); if (i && _arr.length === i) break; } } catch (err) { _d = true; _e = err; } finally { try { if (!_n && _i["return"]) _i["return"](); } finally { if (_d) throw _e; } } return _arr; } return function (arr, i) { if (Array.isArray(arr)) { return arr; } else if (Symbol.iterator in Object(arr)) { return sliceIterator(arr, i); } else { throw new TypeError("Invalid attempt to destructure non-iterable instance"); } }; }();

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

        _this.total_price = "66.66";

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

        _this.set_total_price = function (recipes) {
            if (_this.state.recipes == undefined) {
                return;
            }
            if (recipes == undefined) {
                recipes = _this.state.recipes;
            }
            var price = 0;
            var _iteratorNormalCompletion = true;
            var _didIteratorError = false;
            var _iteratorError = undefined;

            try {
                for (var _iterator = Object.entries(recipes)[Symbol.iterator](), _step; !(_iteratorNormalCompletion = (_step = _iterator.next()).done); _iteratorNormalCompletion = true) {
                    var _ref = _step.value;

                    var _ref2 = _slicedToArray(_ref, 2);

                    var key = _ref2[0];
                    var recipe = _ref2[1];

                    price += recipe.price * recipe.amount;
                }
            } catch (err) {
                _didIteratorError = true;
                _iteratorError = err;
            } finally {
                try {
                    if (!_iteratorNormalCompletion && _iterator.return) {
                        _iterator.return();
                    }
                } finally {
                    if (_didIteratorError) {
                        throw _iteratorError;
                    }
                }
            }

            _this.total_price = price;
        };

        _this.amount_change = _this.amount_change.bind(_this);

        _this.state = {
            date: '...',
            recipes: undefined,
            thumbnail: '',
            order_id: undefined
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
                    order_id: response.order_id
                });
                _this2.set_total_price(response.recipes);
            }).catch(function (error) {
                console.error("Chybyčka: ", error);
            });
        }
    }, {
        key: 'amount_change',
        value: function amount_change(new_amount, id) {
            console.log('In amount change, id:' + id + ', new_amount: ' + new_amount + ', total_price: ' + this.total_price);
            console.log('Attempt to change: ', this.state.recipes[id].amount);
            // this.setState({
            //     recipes: {
            //         ... this.state.recipes,
            //         id: {
            //             ... this.state.recipes[id],
            //             amount: new_amount,
            //         }
            //     }
            // })
            this.setState(function (state) {
                state.recipes[id].amount = new_amount;
                return state;
            });

            console.log('In amount change, id:' + id + ', new_amount: ' + new_amount + ', total_price: ' + this.total_price);
        }
    }, {
        key: 'render',
        value: function render() {

            var recipes = [];
            this.set_total_price();

            if (this.state.recipes != undefined) {
                var _iteratorNormalCompletion2 = true;
                var _didIteratorError2 = false;
                var _iteratorError2 = undefined;

                try {

                    for (var _iterator2 = Object.entries(this.state.recipes)[Symbol.iterator](), _step2; !(_iteratorNormalCompletion2 = (_step2 = _iterator2.next()).done); _iteratorNormalCompletion2 = true) {
                        var _ref3 = _step2.value;

                        var _ref4 = _slicedToArray(_ref3, 2);

                        var key = _ref4[0];
                        var value = _ref4[1];

                        recipes.push(React.createElement(RecipeWidget, {
                            key: key,
                            thumbnail: value.thumbnail,
                            title: value.title,
                            description: value.description,
                            type: value.type,
                            attributes: value.attributes,
                            alergens: value.alergens,
                            amount: value.amount,
                            recipe_order_instance_id: key,
                            price: value.price,
                            onAmountChange: this.amount_change
                        }));
                    }
                } catch (err) {
                    _didIteratorError2 = true;
                    _iteratorError2 = err;
                } finally {
                    try {
                        if (!_iteratorNormalCompletion2 && _iterator2.return) {
                            _iterator2.return();
                        }
                    } finally {
                        if (_didIteratorError2) {
                            throw _iteratorError2;
                        }
                    }
                }
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
                    React.createElement(Cart, { price: this.total_price })
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