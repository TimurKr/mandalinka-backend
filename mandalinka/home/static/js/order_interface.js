var _createClass = function () { function defineProperties(target, props) { for (var i = 0; i < props.length; i++) { var descriptor = props[i]; descriptor.enumerable = descriptor.enumerable || false; descriptor.configurable = true; if ("value" in descriptor) descriptor.writable = true; Object.defineProperty(target, descriptor.key, descriptor); } } return function (Constructor, protoProps, staticProps) { if (protoProps) defineProperties(Constructor.prototype, protoProps); if (staticProps) defineProperties(Constructor, staticProps); return Constructor; }; }();

function _classCallCheck(instance, Constructor) { if (!(instance instanceof Constructor)) { throw new TypeError("Cannot call a class as a function"); } }

function _possibleConstructorReturn(self, call) { if (!self) { throw new ReferenceError("this hasn't been initialised - super() hasn't been called"); } return call && (typeof call === "object" || typeof call === "function") ? call : self; }

function _inherits(subClass, superClass) { if (typeof superClass !== "function" && superClass !== null) { throw new TypeError("Super expression must either be null or a function, not " + typeof superClass); } subClass.prototype = Object.create(superClass && superClass.prototype, { constructor: { value: subClass, enumerable: false, writable: true, configurable: true } }); if (superClass) Object.setPrototypeOf ? Object.setPrototypeOf(subClass, superClass) : subClass.__proto__ = superClass; }

import getCookie from './get_cookie.js';

var OrderInterface = function (_React$Component) {
    _inherits(OrderInterface, _React$Component);

    function OrderInterface(props) {
        _classCallCheck(this, OrderInterface);

        var _this = _possibleConstructorReturn(this, (OrderInterface.__proto__ || Object.getPrototypeOf(OrderInterface)).call(this, props));

        _this.minus_sign_enabled = React.createElement(
            "a",
            { role: "button", onClick: _this.change_portions.bind(_this, -2) },
            React.createElement("i", { className: "bi bi-dash-circle-fill enabled" })
        );
        _this.minus_sign_disabled = React.createElement("i", { className: "bi bi-dash-circle-dotted disabled" });
        _this.plus_sign_enabled = React.createElement(
            "a",
            { role: "button", onClick: _this.change_portions.bind(_this, 2) },
            React.createElement("i", { className: "bi bi-plus-circle-fill enabled" })
        );
        _this.plus_sign_disnabled = React.createElement("i", { className: "bi bi-plus-circle-dotted disabled" });
        _this.loading_button = React.createElement(
            "div",
            { className: "spinner-border spinner-border-sm", role: "status" },
            React.createElement(
                "span",
                { className: "visually-hidden" },
                "Loading..."
            )
        );

        var minus_sign = void 0;
        var plus_sign = void 0;
        var active = void 0;
        if (props.data.value === 0) {
            minus_sign = _this.minus_sign_disabled;
            plus_sign = _this.plus_sign_enabled;
            active = 'inactive';
        } else if (props.data.value > 0) {
            minus_sign = _this.minus_sign_enabled;
            plus_sign = _this.plus_sign_enabled;
            active = 'active';
        } else {
            console.error("Invalid value in OrderInterface");
        };

        _this.state = {
            value: props.data.value,
            class: 'btn btn-primary',
            minus_sign: minus_sign,
            plus_sign: plus_sign,
            active: active,
            recipe_id: props.data.recipe_order_instance_id
        };
        return _this;
    }

    _createClass(OrderInterface, [{
        key: "change_portions",
        value: function change_portions(change) {
            var _this2 = this;

            var put_info = {
                method: 'PUT',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': getCookie('csrftoken')
                },
                body: JSON.stringify({
                    recipe_id: this.state.recipe_id,
                    new_value: this.state.value + change
                }),
                mode: 'same-origin'
            };

            if (change >= 0) {
                this.setState({ plus_sign: this.loading_button });
            } else if (change <= 0) {
                this.setState({ minus_sign: this.loading_button });
            }

            fetch("/edit_order", put_info).then(function (answer) {
                if (answer.status === 200) {
                    // Set value
                    _this2.setState({ value: _this2.state.value + change });

                    if (change >= 0) {
                        _this2.setState({
                            plus_sign: _this2.plus_sign_enabled,
                            minus_sign: _this2.minus_sign_enabled
                        });
                    } else if (change <= 0) {
                        if (_this2.state.value + change <= 0) {
                            _this2.setState({ minus_sign: _this2.minus_sign_disabled });
                        } else {
                            _this2.setState({ minus_sign: _this2.minus_sign_enabled });
                        }
                    }
                } else {
                    console.error(answer);
                }
            }).catch(function (err) {
                console.error("Hej! niečo sa posralo");
                // Tu by sa mal vypísať nejaký error užívatelovi
            });
        }
    }, {
        key: "render",
        value: function render() {

            return React.createElement(
                "div",
                { className: 'hstack gap-2 px-2 bg-primary rounded-pill order-interface allign-middle position-absolute top-0 end-0 translate-middle-y ' + this.state.active },
                this.state.minus_sign,
                React.createElement(
                    "h3",
                    { className: "m-0" },
                    " ",
                    this.state.value,
                    " "
                ),
                this.state.plus_sign
            )

            // <div className="btn-group position-absolute top-0 end-0 translate-middle-y">
            //     <button type="button" className={this.state.class}>-</button>
            //     <button type="button" className={this.state.class}>{this.state.value}</button>
            //     <button type="button" className={this.state.class}>+</button>
            // </div>
            ;
        }
    }]);

    return OrderInterface;
}(React.Component);

export default OrderInterface;