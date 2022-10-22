
// To implement google maps autocomplete functionality on delivery address
"use strict";

function initMap() {
  const CONFIGURATION = {
    "ctaTitle": "Uložiť",
    "mapOptions": { "center": { 'lat': 48.148454532384875, 'lng': 17.10543733560417 }, "fullscreenControl": false, "mapTypeControl": false, "streetViewControl": true, "zoom": 10, "zoomControl": true, "maxZoom": 18, "mapId": "" },
    "mapsApiKey": "AIzaSyCEZTFyo0Kf5YL5SWe6vmmfEMmF5QxSTbU",
    "capabilities": { "addressAutocompleteControl": true, "mapDisplayControl": true, "ctaControl": false }
  };
  const componentForm = [
    'address',
    'district',
    'city',
    'postal',
    'country',
  ];

  const getFormInputElement = (component) => document.getElementById('id_' + component);
  const map = new google.maps.Map(document.getElementById("gmp-map"), {
    zoom: CONFIGURATION.mapOptions.zoom,
    center: CONFIGURATION.mapOptions.center,
    mapTypeControl: CONFIGURATION.mapOptions.mapTypeControl,
    fullscreenControl: CONFIGURATION.mapOptions.fullscreenControl,
    zoomControl: CONFIGURATION.mapOptions.zoomControl,
    streetViewControl: CONFIGURATION.mapOptions.streetViewControl,
    maxZoom: CONFIGURATION.mapOptions.maxZoom,
  });
  const marker = new google.maps.Marker({ map: map, draggable: false });

  const autocompleteInput = getFormInputElement('address');

  const autocomplete = new google.maps.places.Autocomplete(autocompleteInput, {
    fields: ["address_components", "geometry", "name"],
    types: ["address"],
  });

  autocomplete.addListener('place_changed', function () {
    marker.setVisible(false);
    const place = autocomplete.getPlace();
    if (!place.geometry) {
      // User entered the name of a Place that was not suggested and
      // pressed the Enter key, or the Place Details request failed.
      window.alert('No details available for input: \'' + place.name + '\'');
      return;
    }
    renderAddress(place);
    fillInAddress(place);
  });

  // Fill inputs
  function fillInAddress(place) {  // optional parameter
    const addressNameFormat = {
      'street_number': 'short_name',
      'route': 'long_name',
      'locality': 'long_name',
      'sublocality_level_1': 'long_name',
      'country': 'long_name',
      'postal_code': 'short_name',
    };

    const getAddressComp = function (type) {
      for (const component of place.address_components) {
        if (component.types[0] === type) {
          return component[addressNameFormat[type]];
        }
      }
      return '';
    };

    getFormInputElement('address').value =
      getAddressComp('route') + ' ' + getAddressComp('street_number');
    getFormInputElement('district').value = getAddressComp('sublocality_level_1');
    getFormInputElement('city').value = getAddressComp('locality');
    getFormInputElement('postal').value = getAddressComp('postal_code');
    getFormInputElement('country').value = getAddressComp('country');
    getFormInputElement('coordinates').value =
      place.geometry.location.toJSON().lat.toString() + ',' +
      place.geometry.location.toJSON().lng.toString();
  }

  // Render selected location on map
  function renderAddress(place) {
    map.setCenter(place.geometry.location);
    map.setZoom(16);
    marker.setPosition(place.geometry.location);
    marker.setVisible(true);
  }
}
