export default class Attributes extends React.Component {
    render() {
        const attrs = [];
        this.props.attrs.forEach((attr) => {
            attrs.push(
                <a className="attr btn btn-outline-primary" role="button" aria-disabled="true" key={attr}>
                    {attr}
                </a>                    
            )
            
        })
        return (
            <div className="attributes d-flex flex-wrap justify-content-center">
                {attrs}
            </div>
        )
    }
}