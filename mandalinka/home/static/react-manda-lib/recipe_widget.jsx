import Alergens from './alergen_class.js';
import OrderInterface from './order_interface.js';

export default class RecipeWidget extends React.Component {
    constructor(props) {
        super(props);
        const attributes = [];
        props.data.attributes.forEach(attr => {
            attributes.push(
                <div className="m-1 px-2 bg-primary text-light rounded-5 font-size-sm" key={attr}>
                    {attr}
                </div>
            )
        })

        this.state = {
            title: props.data.title,
            description: props.data.description,
            thumbnail: props.data.thumbnail,
            type_color: props.data.type_color,
            attributes: attributes,
            alergens: props.data.alergens,
            order_data: props.data.order_data,
        }
    }

    render() {

        return (
            <div className="col-md-3 col-sm-6 col-6">
                <div className="card position-relative" style={{ background: this.state.type_color }}>
                    <div className="card-body p-2 pb-0">
                        <div className="bg-light rounded-2">
                            <img src={this.state.thumbnail} className="card-img-top rounded-2" alt='img_alt'></img>
                            <h4 className="card-title px-2 mt-2">{this.state.title}</h4>
                            <p className="card-text px-2 m-0">{this.state.description}</p>
                            <div className="d-flex flex-wrap justify-content-center">
                                {this.state.attributes}
                            </div>
                        </div>
                        <Alergens data={this.state.alergens} />
                    </div>
                    <OrderInterface data={this.state.order_data} />
                </div>
            </div>
        )
    }
}

