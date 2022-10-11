import Alergens from './alergens.js';
import OrderInterface from './order_interface.js';
import Attributes from './attributes.js';

export default class RecipeWidget extends React.Component {

	render() {

		return (
			<div className="col-md-3 col-sm-6 col-6">
				<div className={"recipe-widget position-relative " + this.props.type}>
					<div className="card-body p-2 pb-0">
						<div className="bg-light rounded-2 position-relative">
							<img src={this.props.thumbnail} className="card-img-top rounded-2" alt='img_alt'>
							</img>
							<div className='price-tag position-absolute top-0 start-0'>
								{this.props.price + ' €'}
							</div>
							<h4 className="card-title px-2 mt-2">{this.props.title}</h4>
							<p className="card-text px-2 m-0">{this.props.description}</p>
							<Attributes attrs={this.props.attributes} />
						</div>
						<Alergens data={this.props.alergens} />
					</div>
					<OrderInterface 
						amount={this.props.amount}
						recipe_order_instance_id={this.props.recipe_order_instance_id}
						onAmountChange={this.props.onAmountChange} />
				</div>
			</div>
		)
	}
}

