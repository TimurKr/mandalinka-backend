var _createClass = function () { function defineProperties(target, props) { for (var i = 0; i < props.length; i++) { var descriptor = props[i]; descriptor.enumerable = descriptor.enumerable || false; descriptor.configurable = true; if ("value" in descriptor) descriptor.writable = true; Object.defineProperty(target, descriptor.key, descriptor); } } return function (Constructor, protoProps, staticProps) { if (protoProps) defineProperties(Constructor.prototype, protoProps); if (staticProps) defineProperties(Constructor, staticProps); return Constructor; }; }();

function _classCallCheck(instance, Constructor) { if (!(instance instanceof Constructor)) { throw new TypeError("Cannot call a class as a function"); } }

function _possibleConstructorReturn(self, call) { if (!self) { throw new ReferenceError("this hasn't been initialised - super() hasn't been called"); } return call && (typeof call === "object" || typeof call === "function") ? call : self; }

function _inherits(subClass, superClass) { if (typeof superClass !== "function" && superClass !== null) { throw new TypeError("Super expression must either be null or a function, not " + typeof superClass); } subClass.prototype = Object.create(superClass && superClass.prototype, { constructor: { value: subClass, enumerable: false, writable: true, configurable: true } }); if (superClass) Object.setPrototypeOf ? Object.setPrototypeOf(subClass, superClass) : subClass.__proto__ = superClass; }

import getCookie from './get_cookie.js';

function spinner() {
    return React.createElement(
        "div",
        { className: "spinner-border spinner-border-sm", role: "status" },
        React.createElement(
            "span",
            { className: "visually-hidden" },
            "Loading..."
        )
    );
}

var OrderInterface = function (_React$Component) {
    _inherits(OrderInterface, _React$Component);

    function OrderInterface(props) {
        _classCallCheck(this, OrderInterface);

        var _this = _possibleConstructorReturn(this, (OrderInterface.__proto__ || Object.getPrototypeOf(OrderInterface)).call(this, props));

        _this.minus_sign = function () {
            if (_this.props.amount > 0) {
                return React.createElement(
                    "a",
                    { role: "button", onClick: _this.change_portions.bind(_this, -2) },
                    React.createElement("i", { className: "bi bi-dash-lg enabled" })
                );
            } else {
                return React.createElement("i", { className: "bi bi-dash-lg disabled" });
            }
        };

        _this.plus_sign = function () {
            if (_this.props.amount < 0) {
                console.error("Trouble, too low amount");
                return React.createElement("i", { clasName: "bi bi-plus-lg disabled" });
            } else {
                return React.createElement(
                    "a",
                    { className: "p-0 m-0", role: "button", onClick: _this.change_portions.bind(_this, 2) },
                    React.createElement("i", { className: "bi bi-plus-lg enabled" })
                );
            }
        };

        _this.state = {
            loading: false
        };

        return _this;
    }

    _createClass(OrderInterface, [{
        key: "change_portions",
        value: function change_portions(change) {
            var _this2 = this;

            var new_amount = this.props.amount + change;
            var put_info = {
                method: 'PUT',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': getCookie('csrftoken')
                },
                body: JSON.stringify({
                    recipe_id: this.props.recipe_order_instance_id,
                    new_amount: new_amount
                }),
                mode: 'same-origin'
            };

            this.setState({ loading: true });

            fetch("/edit_order", put_info).then(function (answer) {
                if (answer.status === 200) {
                    console.log("Juchu, dostal som odpoveď 200");
                    _this2.props.onAmountChange(new_amount, _this2.props.recipe_order_instance_id);
                    // this.setState({loading: false});
                } else {
                    console.error(answer);
                }
            }).catch(function (err) {
                console.error("Hej! niečo sa posralo", err);
                // Tu by sa mal vypísať nejaký error užívatelovi
            });
        }
    }, {
        key: "render",
        value: function render() {
            return React.createElement(
                "div",
                {
                    className: "hstack order-interface allign-middle position-absolute top-0 end-0 translate-middle-y  " + (this.props.amount > 0 ? 'active' : 'inactive') },
                this.minus_sign(),
                this.state.loading ? spinner() : React.createElement(
                    "h3",
                    null,
                    " ",
                    this.props.amount,
                    " "
                ),
                this.plus_sign()
            );
        }
    }]);

    return OrderInterface;
}(React.Component);

export default OrderInterface;