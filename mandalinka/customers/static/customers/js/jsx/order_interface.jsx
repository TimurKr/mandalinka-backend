import getCookie from './get_cookie.js';

function Spinner(){
    return  <div className="spinner-border spinner-border-sm" role="status">
                <span className="visually-hidden">Loading...</span>
            </div>
}

export default class OrderInterface extends React.Component {
    
    constructor(props) {
        super(props);

        this.state = {
            loading: false,
        };

    }

    change_portions(change){ 
        const new_amount = this.props.amount + change;
        const put_info = {
            method: 'PUT',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCookie('csrftoken'),
            },
            body: JSON.stringify({
                recipe_id: this.props.recipe_order_instance_id,
                new_amount: new_amount,
            }),
            mode: 'same-origin',
        };
        
        this.setState({loading: true})

        fetch(`/edit_order`, put_info)
        .then((answer) => {
            if (answer.status === 200) {
                this.props.onAmountChange(new_amount, this.props.recipe_order_instance_id);
                this.setState({loading: false});
            } else {
                console.error(answer);
            }
        })
        .catch((err) => {
            console.error("Hej! niečo sa posralo", err)
            // Tu by sa mal vypísať nejaký error užívatelovi
        })
    }

    minus_sign = () => {
        if (this.props.amount > 0) {
            return (
                <a role="button" onClick={this.change_portions.bind(this, -2)}>
                    <i className="bi bi-dash-lg enabled"></i>
                </a>
            )
        } else {
            return (
                <i className="bi bi-dash-lg disabled"></i>
            )
        }
    }

    plus_sign = () => {
        if (this.props.amount < 0) {
            console.error("Trouble, too low amount");
            return (
                <i clasName="bi bi-plus-lg disabled"></i>
            )
        } else {
            return (
                <a className="p-0 m-0" role="button" onClick={this.change_portions.bind(this, 2)}>
                    <i className="bi bi-plus-lg enabled"></i>
                </a>
            )
        }
    }

    
    render() {
        return (
            <div 
                className={`hstack order-interface allign-middle position-absolute top-0 end-0 translate-middle-y  ${this.props.amount > 0 ? 'active' : 'inactive'}`}>
                {this.minus_sign()}
                { 
                    this.state.loading
                    ? <Spinner/>
                    : <h3> {this.props.amount} </h3>
                }
                {this.plus_sign()}
            </div>
        )
    }
}