var _slicedToArray = function () { function sliceIterator(arr, i) { var _arr = []; var _n = true; var _d = false; var _e = undefined; try { for (var _i = arr[Symbol.iterator](), _s; !(_n = (_s = _i.next()).done); _n = true) { _arr.push(_s.value); if (i && _arr.length === i) break; } } catch (err) { _d = true; _e = err; } finally { try { if (!_n && _i["return"]) _i["return"](); } finally { if (_d) throw _e; } } return _arr; } return function (arr, i) { if (Array.isArray(arr)) { return arr; } else if (Symbol.iterator in Object(arr)) { return sliceIterator(arr, i); } else { throw new TypeError("Invalid attempt to destructure non-iterable instance"); } }; }();

var _createClass = function () { function defineProperties(target, props) { for (var i = 0; i < props.length; i++) { var descriptor = props[i]; descriptor.enumerable = descriptor.enumerable || false; descriptor.configurable = true; if ("value" in descriptor) descriptor.writable = true; Object.defineProperty(target, descriptor.key, descriptor); } } return function (Constructor, protoProps, staticProps) { if (protoProps) defineProperties(Constructor.prototype, protoProps); if (staticProps) defineProperties(Constructor, staticProps); return Constructor; }; }();

function _classCallCheck(instance, Constructor) { if (!(instance instanceof Constructor)) { throw new TypeError("Cannot call a class as a function"); } }

function _possibleConstructorReturn(self, call) { if (!self) { throw new ReferenceError("this hasn't been initialised - super() hasn't been called"); } return call && (typeof call === "object" || typeof call === "function") ? call : self; }

function _inherits(subClass, superClass) { if (typeof superClass !== "function" && superClass !== null) { throw new TypeError("Super expression must either be null or a function, not " + typeof superClass); } subClass.prototype = Object.create(superClass && superClass.prototype, { constructor: { value: subClass, enumerable: false, writable: true, configurable: true } }); if (superClass) Object.setPrototypeOf ? Object.setPrototypeOf(subClass, superClass) : subClass.__proto__ = superClass; }

function JsxAttribute(props) {
	var className = 'attr btn btn-outline-primary ' + (props.selected ? 'selected ' : '') + (props.favorite ? 'favorite ' : '') + (props.type != undefined ? props.type : '');

	return React.createElement(
		'a',
		{
			className: className, role: 'button', 'aria-disabled': 'true', key: props.title },
		props.title
	);
}

var Attributes = function (_React$Component) {
	_inherits(Attributes, _React$Component);

	function Attributes() {
		_classCallCheck(this, Attributes);

		return _possibleConstructorReturn(this, (Attributes.__proto__ || Object.getPrototypeOf(Attributes)).apply(this, arguments));
	}

	_createClass(Attributes, [{
		key: 'render',
		value: function render() {
			var attr_type = React.createElement(JsxAttribute, {
				title: this.props.type,
				selected: false,
				favorite: false,
				type: this.props.type
			});

			var attrs_fav_sel = [];
			var attrs_sel = [];
			var attrs_fav = [];
			var attrs_rest = [];

			var _iteratorNormalCompletion = true;
			var _didIteratorError = false;
			var _iteratorError = undefined;

			try {
				for (var _iterator = Object.entries(this.props.attrs)[Symbol.iterator](), _step; !(_iteratorNormalCompletion = (_step = _iterator.next()).done); _iteratorNormalCompletion = true) {
					var _ref = _step.value;

					var _ref2 = _slicedToArray(_ref, 2);

					var key = _ref2[0];
					var value = _ref2[1];


					if (value.favorite && value.selected) {
						attrs_fav_sel.push(React.createElement(JsxAttribute, {
							title: key,
							selected: value.selected,
							favorite: value.favorite,
							key: key
						}));
					} else if (value.selected) {
						attrs_sel.push(React.createElement(JsxAttribute, {
							title: key,
							selected: value.selected,
							favorite: value.favorite,
							key: key
						}));
					} else if (value.favorite) {
						attrs_fav.push(React.createElement(JsxAttribute, {
							title: key,
							selected: value.selected,
							favorite: value.favorite,
							key: key
						}));
					} else {
						attrs_rest.push(React.createElement(JsxAttribute, {
							title: key,
							selected: value.selected,
							favorite: value.favorite,
							key: key
						}));
					}
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

			return React.createElement(
				'div',
				{ className: 'attributes d-flex flex-wrap justify-content-center' },
				attr_type,
				attrs_fav_sel,
				attrs_sel,
				attrs_fav,
				attrs_rest
			);
		}
	}]);

	return Attributes;
}(React.Component);

export default Attributes;