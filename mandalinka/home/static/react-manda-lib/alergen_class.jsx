export default class Alergens extends React.Component {
    constructor(props) {
        super(props);
        this.state = {allergens: props.data}
    }

    get_print_codes(list) {
        let print_codes = []
        list.forEach(allergen => {
            print_codes.push(allergen[0])
        })
        if (print_codes.length == 0) {
            return 'Žiadne alergény'
        }
        return 'Alergény: ' + print_codes.join(', ')
    }

    render(){
        return (
            <div>
                <p className="text-end m-0 p-1">{this.get_print_codes(this.state.allergens)}</p>
            </div>
        )
    }
}