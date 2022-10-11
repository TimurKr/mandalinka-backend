var _createClass = function () { function defineProperties(target, props) { for (var i = 0; i < props.length; i++) { var descriptor = props[i]; descriptor.enumerable = descriptor.enumerable || false; descriptor.configurable = true; if ("value" in descriptor) descriptor.writable = true; Object.defineProperty(target, descriptor.key, descriptor); } } return function (Constructor, protoProps, staticProps) { if (protoProps) defineProperties(Constructor.prototype, protoProps); if (staticProps) defineProperties(Constructor, staticProps); return Constructor; }; }();

function _classCallCheck(instance, Constructor) { if (!(instance instanceof Constructor)) { throw new TypeError("Cannot call a class as a function"); } }

function _possibleConstructorReturn(self, call) { if (!self) { throw new ReferenceError("this hasn't been initialised - super() hasn't been called"); } return call && (typeof call === "object" || typeof call === "function") ? call : self; }

function _inherits(subClass, superClass) { if (typeof superClass !== "function" && superClass !== null) { throw new TypeError("Super expression must either be null or a function, not " + typeof superClass); } subClass.prototype = Object.create(superClass && superClass.prototype, { constructor: { value: subClass, enumerable: false, writable: true, configurable: true } }); if (superClass) Object.setPrototypeOf ? Object.setPrototypeOf(subClass, superClass) : subClass.__proto__ = superClass; }

import Alergens from './alergens.js';
import OrderInterface from './order_interface.js';
import Attributes from './attributes.js';
import PriceTag from './price_tag.js';

var RecipeWidget = function (_React$Component) {
	_inherits(RecipeWidget, _React$Component);

	function RecipeWidget() {
		_classCallCheck(this, RecipeWidget);

		return _possibleConstructorReturn(this, (RecipeWidget.__proto__ || Object.getPrototypeOf(RecipeWidget)).apply(this, arguments));
	}

	_createClass(RecipeWidget, [{
		key: 'render',
		value: function render() {

			return React.createElement(
				'div',
				{ className: 'col-md-3 col-sm-6 col-6' },
				React.createElement(
					'div',
					{ className: "recipe-widget position-relative " + this.props.type },
					React.createElement(
						'div',
						{ className: 'card-body p-2 pb-0' },
						React.createElement(
							'div',
							{ className: 'bg-light rounded-2 position-relative' },
							React.createElement('img', { src: this.props.thumbnail, className: 'card-img-top rounded-2', alt: 'img_alt' }),
							React.createElement(
								'div',
								{ className: "price-tag position-absolute top-0 start-0 " + this.props.type },
								React.createElement(PriceTag, { price: this.props.price })
							),
							React.createElement(
								'h4',
								{ className: 'card-title px-2 mt-2' },
								this.props.title
							),
							React.createElement(
								'p',
								{ className: 'card-text px-2 m-0' },
								this.props.description
							),
							React.createElement(Attributes, { attrs: this.props.attributes })
						),
						React.createElement(Alergens, { data: this.props.alergens })
					),
					React.createElement(OrderInterface, {
						amount: this.props.amount,
						recipe_order_instance_id: this.props.recipe_order_instance_id,
						onAmountChange: this.props.onAmountChange })
				)
			);
		}
	}]);

	return RecipeWidget;
}(React.Component);

export default RecipeWidget;