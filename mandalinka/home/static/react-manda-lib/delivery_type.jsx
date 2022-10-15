export default function DeliveryType(props) {
    let pickup, delivery;
    if (props.pickup) {
        pickup = 
            <a className="active">
                <span className="material-symbols-rounded md-36 fill">
                    pedal_bike
                </span>
            </a>
        delivery = 
            <a href="#" onClick={props.toggle} className='inactive'>
                <span className="material-symbols-rounded md-36">
                    storefront
                </span>
            </a>
    } else {
        pickup = 
            <a href="#" onClick={props.toggle} className="inactive">
                <span className="material-symbols-rounded md-36">
                    pedal_bike
                </span>
            </a>
        delivery = 
            <a className='active'>
                <span className="material-symbols-rounded md-36 fill">
                    storefront
                </span>
            </a>
    }
    return  <div className="delivery-type hstack">
                {pickup}
                <div className="vr"></div>
                {delivery}
            </div>;


}