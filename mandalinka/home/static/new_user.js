document.addEventListener("DOMContentLoaded", function () {
  
  // Form validation
  const SignupForm = document.getElementById('NewUserForm')
  
  SignupForm.addEventListener('submit', event => {
    if (!SignupForm.checkValidity()) {
      event.preventDefault();
      event.stopPropagation();
    }
    SignupForm.classList.add('was-validated');
  }, false)
  
  
  // // Code for tab < > buttons
  // // Mapping to next tab
  // document.querySelector('#btn-next').onclick = function () {
  //   document.querySelector('.nav .active').parentElement.nextElementSibling.querySelector('button').click()
  // };
  // // Mapping to prev tabs
  // document.querySelector('#btn-prev').onclick = function () {
  //   document.querySelector('.nav .active').parentElement.previousElementSibling.querySelector('button').click()
  // };

  // const tabs = document.querySelectorAll('.nav li');
  // const btnNext = document.querySelector('#btn-next');
  // const btnPrev = document.querySelector('#btn-prev');
  // const btnSubm = document.querySelector('#submit')

  // // Disable and enable < > buttons for first and last
  // tabs.forEach(function (tab) {
  //   let button = tab.querySelector('button');
  //   if (tab === tabs[0]) {
  //     button.onclick = function () {
  //       btnPrev.setAttribute('disabled', '');
  //       btnNext.removeAttribute('disabled');
  //       btnSubm.setAttribute('hidden', '');
  //       scroll(top);
  //     }
  //   } else if (tab === tabs[tabs.length - 1]) {
  //     button.onclick = function () {
  //       btnNext.setAttribute('disabled', '');
  //       btnPrev.removeAttribute('disabled');
  //       btnSubm.removeAttribute('hidden');
  //       scroll(top);
  //     }
  //   } else {
  //     button.onclick = function () {
  //       btnNext.removeAttribute('disabled');
  //       btnPrev.removeAttribute('disabled');
  //       btnSubm.setAttribute('hidden', '');
  //       scroll(top);
  //     }
  //   }
  // });

});


// // To implement google maps autocomplete functionality on delivery address
// "use strict";

// function initMap() {
//   const CONFIGURATION = {
//     "ctaTitle": "Uložiť",
//     "mapOptions": { "center": { 'lat': 48.148454532384875, 'lng': 17.10543733560417}, "fullscreenControl": false, "mapTypeControl": false, "streetViewControl": true, "zoom": 10, "zoomControl": true, "maxZoom": 18, "mapId": "" },
//     "mapsApiKey": "AIzaSyCEZTFyo0Kf5YL5SWe6vmmfEMmF5QxSTbU",
//     "capabilities": { "addressAutocompleteControl": true, "mapDisplayControl": true, "ctaControl": false }
//   };
//   const componentForm = [
//     'address',
//     'district',
//     'city',
//     'postal',
//     'country',
//   ];

//   const getFormInputElement = (component) => document.getElementById('id_' + component);
//   const map = new google.maps.Map(document.getElementById("gmp-map"), {
//     zoom: CONFIGURATION.mapOptions.zoom,
//     center: CONFIGURATION.mapOptions.center,
//     mapTypeControl: CONFIGURATION.mapOptions.mapTypeControl,
//     fullscreenControl: CONFIGURATION.mapOptions.fullscreenControl,
//     zoomControl: CONFIGURATION.mapOptions.zoomControl,
//     streetViewControl: CONFIGURATION.mapOptions.streetViewControl,
//     maxZoom: CONFIGURATION.mapOptions.maxZoom,
//   });
//   const marker = new google.maps.Marker({ map: map, draggable: false });
  
//   const autocompleteInput = getFormInputElement('address');

//   const autocomplete = new google.maps.places.Autocomplete(autocompleteInput, {
//     fields: ["address_components", "geometry", "name"],
//     types: ["address"],
//   });

//   autocomplete.addListener('place_changed', function () {
//     marker.setVisible(false);
//     const place = autocomplete.getPlace();
//     if (!place.geometry) {
//       // User entered the name of a Place that was not suggested and
//       // pressed the Enter key, or the Place Details request failed.
//       window.alert('No details available for input: \'' + place.name + '\'');
//       return;
//     }
//     renderAddress(place);
//     fillInAddress(place);
//   });

//   // Fill inputs
//   function fillInAddress(place) {  // optional parameter
//     const addressNameFormat = {
//       'street_number': 'short_name',
//       'route': 'long_name',
//       'locality': 'long_name',
//       'sublocality_level_1': 'long_name',
//       'country': 'long_name',
//       'postal_code': 'short_name',
//     };

//     const getAddressComp = function (type) {
//       for (const component of place.address_components) {
//         if (component.types[0] === type) {
//           return component[addressNameFormat[type]];
//         }
//       }
//       return '';
//     };

//     getFormInputElement('address').value =
//       getAddressComp('route') + ' ' + getAddressComp('street_number');
//     getFormInputElement('district').value = getAddressComp('sublocality_level_1');
//     getFormInputElement('city').value = getAddressComp('locality');
//     getFormInputElement('postal').value = getAddressComp('postal_code');
//     getFormInputElement('country').value = getAddressComp('country');
//     getFormInputElement('coordinates').value = 
//       place.geometry.location.toJSON().lat.toString() + ',' + 
//       place.geometry.location.toJSON().lng.toString();
//   }

//   // Render selected location on map
//   function renderAddress(place) {
//     map.setCenter(place.geometry.location);
//     map.setZoom(16);
//     marker.setPosition(place.geometry.location);
//     marker.setVisible(true);
//   }
// }