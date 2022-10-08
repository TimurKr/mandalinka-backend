var _createClass = function () { function defineProperties(target, props) { for (var i = 0; i < props.length; i++) { var descriptor = props[i]; descriptor.enumerable = descriptor.enumerable || false; descriptor.configurable = true; if ("value" in descriptor) descriptor.writable = true; Object.defineProperty(target, descriptor.key, descriptor); } } return function (Constructor, protoProps, staticProps) { if (protoProps) defineProperties(Constructor.prototype, protoProps); if (staticProps) defineProperties(Constructor, staticProps); return Constructor; }; }();

function _classCallCheck(instance, Constructor) { if (!(instance instanceof Constructor)) { throw new TypeError("Cannot call a class as a function"); } }

function _possibleConstructorReturn(self, call) { if (!self) { throw new ReferenceError("this hasn't been initialised - super() hasn't been called"); } return call && (typeof call === "object" || typeof call === "function") ? call : self; }

function _inherits(subClass, superClass) { if (typeof superClass !== "function" && superClass !== null) { throw new TypeError("Super expression must either be null or a function, not " + typeof superClass); } subClass.prototype = Object.create(superClass && superClass.prototype, { constructor: { value: subClass, enumerable: false, writable: true, configurable: true } }); if (superClass) Object.setPrototypeOf ? Object.setPrototypeOf(subClass, superClass) : subClass.__proto__ = superClass; }

import Alergens from './alergen_class.js';
import OrderInterface from './order_interface.js';

var RecipeWidget = function (_React$Component) {
    _inherits(RecipeWidget, _React$Component);

    function RecipeWidget(props) {
        _classCallCheck(this, RecipeWidget);

        var _this = _possibleConstructorReturn(this, (RecipeWidget.__proto__ || Object.getPrototypeOf(RecipeWidget)).call(this, props));

        var attributes = [];
        props.data.attributes.forEach(function (attr) {
            attributes.push(React.createElement(
                'div',
                { className: 'm-1 px-2 bg-primary text-light rounded-5 font-size-sm', key: attr },
                attr
            ));
        });

        _this.state = {
            title: props.data.title,
            description: props.data.description,
            thumbnail: props.data.thumbnail,
            type_color: props.data.type_color,
            attributes: attributes,
            alergens: props.data.alergens,
            order_data: props.data.order_data
        };
        return _this;
    }

    _createClass(RecipeWidget, [{
        key: 'render',
        value: function render() {

            return React.createElement(
                'div',
                { className: 'col-md-3 col-sm-6 col-6' },
                React.createElement(
                    'div',
                    { className: 'card position-relative', style: { background: this.state.type_color } },
                    React.createElement(
                        'div',
                        { className: 'card-body p-2 pb-0' },
                        React.createElement(
                            'div',
                            { className: 'bg-light rounded-2' },
                            React.createElement('img', { src: this.state.thumbnail, className: 'card-img-top rounded-2', alt: 'img_alt' }),
                            React.createElement(
                                'h4',
                                { className: 'card-title px-2 mt-2' },
                                this.state.title
                            ),
                            React.createElement(
                                'p',
                                { className: 'card-text px-2 m-0' },
                                this.state.description
                            ),
                            React.createElement(
                                'div',
                                { className: 'd-flex flex-wrap justify-content-center' },
                                this.state.attributes
                            )
                        ),
                        React.createElement(Alergens, { data: this.state.alergens })
                    ),
                    React.createElement(OrderInterface, { data: this.state.order_data })
                )
            );
        }
    }]);

    return RecipeWidget;
}(React.Component);

export default RecipeWidget;