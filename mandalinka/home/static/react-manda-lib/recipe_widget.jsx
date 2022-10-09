import Alergens from './alergens.jsx';
import OrderInterface from './order_interface.js';
import Attributes from './attributes.js';

export default class RecipeWidget extends React.Component {
    
    render() {

        return (
            <div className="col-md-3 col-sm-6 col-6">
                <div className={"recipe-widget position-relative " + this.props.type}>
                    <div className="card-body p-2 pb-0">
                        <div className="bg-light rounded-2">
                            <img src={this.props.thumbnail} className="card-img-top rounded-2" alt='img_alt'></img>
                            <h4 className="card-title px-2 mt-2">{this.props.title}</h4>
                            <p className="card-text px-2 m-0">{this.props.description}</p>
                            <Attributes attrs={this.props.attributes}/>
                        </div>
                        <Alergens data={this.props.alergens} />
                    </div>
                    <OrderInterface data={this.props.order_data} />
                </div>
            </div>
        )
    }
}

