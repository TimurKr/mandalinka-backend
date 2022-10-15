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
            order_id: undefined,
            attributes: undefined
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
                    attributes: response.attributes
                });
                _this2.set_total_price(response.recipes);
            }).catch(function (error) {
                console.error("Chybyčka: ", error);
            });
        }
    }, {
        key: 'amount_change',
        value: function amount_change(new_amount, id) {
            this.setState(function (state) {
                state.recipes[id].amount = new_amount;
                return state;
            });
        }
    }, {
        key: 'render',
        value: function render() {

            var recipes = {};
            this.set_total_price();

            if (this.state.recipes != undefined) {
                var _iteratorNormalCompletion2 = true;
                var _didIteratorError2 = false;
                var _iteratorError2 = undefined;

                try {

                    for (var _iterator2 = Object.entries(this.state.recipes)[Symbol.iterator](), _step2; !(_iteratorNormalCompletion2 = (_step2 = _iterator2.next()).done); _iteratorNormalCompletion2 = true) {
                        var _ref3 = _step2.value;

                        var _ref4 = _slicedToArray(_ref3, 2);

                        var rec_key = _ref4[0];
                        var rec_data = _ref4[1];


                        var recipe_attributes = {};
                        var _iteratorNormalCompletion3 = true;
                        var _didIteratorError3 = false;
                        var _iteratorError3 = undefined;

                        try {
                            for (var _iterator3 = Object.entries(this.state.attributes)[Symbol.iterator](), _step3; !(_iteratorNormalCompletion3 = (_step3 = _iterator3.next()).done); _iteratorNormalCompletion3 = true) {
                                var _ref5 = _step3.value;

                                var _ref6 = _slicedToArray(_ref5, 2);

                                var attr_key = _ref6[0];
                                var attr_data = _ref6[1];

                                if (attr_data.recipes.includes(rec_key)) {
                                    recipe_attributes[attr_key] = {
                                        favorite: attr_data.favorite,
                                        selected: attr_data.selected
                                    };
                                }
                            }
                        } catch (err) {
                            _didIteratorError3 = true;
                            _iteratorError3 = err;
                        } finally {
                            try {
                                if (!_iteratorNormalCompletion3 && _iterator3.return) {
                                    _iterator3.return();
                                }
                            } finally {
                                if (_didIteratorError3) {
                                    throw _iteratorError3;
                                }
                            }
                        }

                        if (recipes[rec_data.type] === undefined) {
                            recipes[rec_data.type] = [];
                        }
                        recipes[rec_data.type].push(React.createElement(RecipeWidget, {
                            key: rec_key,
                            thumbnail: rec_data.thumbnail,
                            title: rec_data.title,
                            description: rec_data.description,
                            type: rec_data.type,
                            attributes: recipe_attributes,
                            alergens: rec_data.alergens,
                            amount: rec_data.amount,
                            recipe_order_instance_id: rec_key,
                            price: rec_data.price,
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

            var final_recipes = [];
            var _iteratorNormalCompletion4 = true;
            var _didIteratorError4 = false;
            var _iteratorError4 = undefined;

            try {
                for (var _iterator4 = Object.keys(recipes).sort().reverse()[Symbol.iterator](), _step4; !(_iteratorNormalCompletion4 = (_step4 = _iterator4.next()).done); _iteratorNormalCompletion4 = true) {
                    var type = _step4.value;

                    final_recipes.push(React.createElement(
                        'div',
                        { key: type, className: 'col-md-3 col-12' },
                        recipes[type]
                    ));
                }
            } catch (err) {
                _didIteratorError4 = true;
                _iteratorError4 = err;
            } finally {
                try {
                    if (!_iteratorNormalCompletion4 && _iterator4.return) {
                        _iterator4.return();
                    }
                } finally {
                    if (_didIteratorError4) {
                        throw _iteratorError4;
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
                    React.createElement(
                        'div',
                        { className: 'd-inline-flex align-items-center' },
                        React.createElement(DeliveryType, { pickup: this.state.pickup, toggle: this.toggle_pickup }),
                        React.createElement(Cart, { price: this.total_price })
                    )
                ),
                React.createElement(
                    'div',
                    { className: 'row gx-3 gy-4' },
                    final_recipes
                )
            );
        }
    }]);

    return OrderEditing;
}(React.Component);

root.render(React.createElement(OrderEditing, null));