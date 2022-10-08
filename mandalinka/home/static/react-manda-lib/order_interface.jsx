import getCookie from './get_cookie.js';

export default class OrderInterface extends React.Component {
    
    constructor(props) {
        super(props);

        this.minus_sign_enabled = 
            <a role="button" onClick={this.change_portions.bind(this, -2)}>
                <i className="bi bi-dash-circle-fill enabled"/>
            </a>
        this.minus_sign_disabled = 
            <i className="bi bi-dash-circle-dotted disabled"/>
        this.plus_sign_enabled = 
            <a role="button" onClick={this.change_portions.bind(this, 2)}>
                <i className="bi bi-plus-circle-fill enabled"/>
            </a>
        this.plus_sign_disnabled = 
            <i className="bi bi-plus-circle-dotted disabled"/>
        this.loading_button = 
            <div className="spinner-border spinner-border-sm" role="status">
                <span className="visually-hidden">Loading...</span>
            </div>

        let minus_sign;
        let plus_sign;
        let active;
        if (props.data.value === 0) {
            minus_sign = this.minus_sign_disabled;
            plus_sign = this.plus_sign_enabled;
            active = 'inactive'
        } else if (props.data.value > 0) {
            minus_sign = this.minus_sign_enabled;
            plus_sign = this.plus_sign_enabled;
            active = 'active';
        } else {
            console.error("Invalid value in OrderInterface");
        };

        this.state = {
            value: props.data.value,
            class: 'btn btn-primary',
            minus_sign: minus_sign,
            plus_sign: plus_sign,
            active: active,
            recipe_id: props.data.recipe_order_instance_id,
        };
    }

    change_portions(change) { 
        const put_info = {
            method: 'PUT',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCookie('csrftoken'),
            },
            body: JSON.stringify({
                recipe_id: this.state.recipe_id,
                new_value: this.state.value + change,
            }),
            mode: 'same-origin',
        };

        if (change >= 0) {
            this.setState({plus_sign: this.loading_button})
        } else if (change <= 0) {
            this.setState({minus_sign: this.loading_button})
        }

        fetch(`/edit_order`, put_info)
        .then((answer) => {
            if (answer.status === 200) {
                // Set value
                this.setState({value: this.state.value + change});

                if (change >= 0) {
                    this.setState({
                        plus_sign: this.plus_sign_enabled,
                        minus_sign: this.minus_sign_enabled
                    })
                } else if (change <= 0) {
                    if (this.state.value + change <= 0) {
                        this.setState({minus_sign: this.minus_sign_disabled})
                    } else {
                        this.setState({minus_sign: this.minus_sign_enabled})
                    }  
                }
            } else {
                console.error(answer)
            }
        })
        .catch((err) => {
            console.error("Hej! niečo sa posralo")
            // Tu by sa mal vypísať nejaký error užívatelovi
        })
    }

    render() {
        
        return (
            <div className={'hstack gap-2 px-2 bg-primary rounded-pill order-interface allign-middle position-absolute top-0 end-0 translate-middle-y ' + this.state.active}>
                {this.state.minus_sign}
                <h3 className="m-0"> {this.state.value} </h3>
                {this.state.plus_sign}
            </div>

            // <div className="btn-group position-absolute top-0 end-0 translate-middle-y">
            //     <button type="button" className={this.state.class}>-</button>
            //     <button type="button" className={this.state.class}>{this.state.value}</button>
            //     <button type="button" className={this.state.class}>+</button>
            // </div>
        )
    }
}