import React from "react";
import { useState, useEffect } from "react";
import { useImmer } from "use-immer";
import parse from "html-react-parser";
import getCookie from "./get_cookie.jsx";

function IngredietInfoPanel({ data }) {
  return <div className="col info">Tu raz bude niečo o ingrediencií</div>;
}
function VersionInfoPanel({ data }) {
  return (
    <div className={"ingredient-version-info-" + data.id}>
      <h3>
        {data.ingredient} v.{data.version_number}
      </h3>
      {data.active ? <p>Aktívne od {data.status_changed}</p> : null}
      {data.inactive ? <p>V príprave od {data.status_changed}</p> : null}
      {data.deleted ? <p>Odstránené {data.status_changed}</p> : null}
      <p></p>
      <p>
        Cena:{" "}
        <strong>
          {data.cost} € / {data.unit.sign}
        </strong>
      </p>
      <p>
        Dodávateľ: <strong>{data.source}</strong>
      </p>

      <p>
        Na sklade: <strong>{data.in_stock} </strong>
      </p>

      <p>
        Vyrobené dňa: <strong>{data.created}</strong>
      </p>
      <p>
        Posledná zmena: <strong>{data.last_modified}</strong>
      </p>

      {data.active ? (
        <div className="actions row justify-content-end">
          <button className="btn success-light-button col-auto">
            Objednať
          </button>
          <button className="btn dark-light-button col-auto">Odpísať</button>
          <button className="btn danger-light-button col-auto">
            Deaktivavať
          </button>
          <button className="btn danger-button col-auto">Vymazať</button>
        </div>
      ) : null}
      {data.inactive ? (
        <div className="actions row justify-content-end">
          {data.in_stock != 0 ? (
            <button className="btn dark-light-button col-auto">Odpísať</button>
          ) : null}
          <button className="btn success-light-button ms-auto col-auto">
            Aktivovať
          </button>
          <button className="btn danger-button col-auto">Vymazať</button>
        </div>
      ) : null}
      {data.deleted ? (
        <div className="actions row justify-content-end">
          <button className="btn success-light-button ms-auto col-auto">
            Obnoviť
          </button>
        </div>
      ) : null}
    </div>
  );
}

function NewVersionFormPanel({ children, on_submit, hidden = false }) {
  return (
    <form
      id="new-ingredient-version-form-"
      method="POST"
      onSubmit={on_submit}
      hidden={hidden}
    >
      {children}
    </form>
  );
}

function VersionsPanel({ versions, showVersionInfo, showNewVersionForm }) {
  return (
    <div>
      <p className="versions-title">Verzie</p>
      <hr></hr>
      {versions.map((version) => (
        <div className="version-buttons" key={version.id}>
          <p
            className={
              "version-button " +
              version.status +
              " " +
              (version.selected ? "selected" : "")
            }
            onClick={() => showVersionInfo(version.id)}
            version-id={version.pk}
          >
            {version.ingredient} v. {version.version_number}
          </p>
        </div>
      ))}
      <button
        className="btn success-light-button add-version-button"
        onClick={showNewVersionForm}
      >
        Pridať verziu
      </button>
    </div>
  );
}

export default function IngredientWidget({ ingredient, url }) {
  const [showModal, setShowModal] = useState(false);
  const [modal, setModal] = useState(null);
  const [loaded, setLoaded] = useState(false);

  const [infoPanel, setInfoPanel] = useState(<IngredietInfoPanel />);
  const [versions, setVersions] = useImmer(ingredient.versions);

  function showIngredientInfo(event) {
    setVersions((draft) => {
      draft.forEach((version) => {
        version.selected = false;
      });
    });
    setInfoPanel(<IngredietInfoPanel data={ingredient} />);
  }

  function showVersionInfo(version_id) {
    if (!loaded) {
      console.log("Versions not loaded yet");
      return;
    }
    setVersions((draft) => {
      draft.forEach((version) => {
        if (version.id == version_id) {
          version.selected = true;
        } else {
          version.selected = false;
        }
      });
    });
    versions.forEach((version) => {
      if (version.id == version_id) {
        setInfoPanel(<VersionInfoPanel data={version} />);
        return;
      }
    });
  }

  function showNewVersionForm(event) {
    setVersions((draft) => {
      draft.forEach((version) => {
        version.selected = false;
      });
    });
    setInfoPanel(null);
  }

  function loadVersions() {
    fetch(url + "?id=" + ingredient.id, {
      method: "GET",
      mode: "same-origin",
      headers: {
        "Content-Type": "application/json",
        "X-CSRFToken": getCookie("csrftoken"),
      },
    })
      .then((response) => response.json())
      .then((response) => {
        setVersions(response);
        console.log("Fetched versions: ", response);
        setLoaded(true);
      })
      .catch((error) => {
        console.log("Couldnt fetch: ", error);
      });
  }

  function submitNewVersion(e) {
    e.preventDefault();
    console.log("New version form submitting.");
  }

  useEffect(() => {
    if (!modal) {
      console.log("Creating modal");
      setModal(
        new bootstrap.Modal("#modal-" + ingredient.id, { backdrop: "static" })
      );
      return;
    }
    if (showModal) {
      console.log("Showing modal");
      modal.show();
      if (!loaded) loadVersions();
    } else {
      console.log("Hiding modal");
      modal.hide();
    }
  }, [showModal, modal]);

  return (
    <div className="ingredient-widget">
      <p
        className={"ingredient-button active"}
        onClick={() => setShowModal(true)}
      >
        {ingredient["name"]}
      </p>

      <div
        className="modal fade modal-lg ingredient-modal"
        id={"modal-" + ingredient.id}
        tabIndex="-1"
        aria-labelledby={"modal-" + ingredient.id + "-title"}
        aria-hidden="true"
      >
        <div className="modal-dialog modal-xl">
          <div className="modal-content">
            <div className="modal-header">
              <button
                type="button"
                className="btn-close"
                onClick={() => setShowModal(false)}
              ></button>
            </div>
            <div className="modal-body row">
              <div className="versions col-auto">
                <h2
                  id={"modal-" + ingredient.id + "-title"}
                  className="ingredient-title"
                  onClick={showIngredientInfo}
                >
                  {ingredient.name}
                </h2>
                <VersionsPanel
                  versions={versions}
                  showVersionInfo={showVersionInfo}
                  showNewVersionForm={showNewVersionForm}
                />
              </div>
              <div className="col info">
                {infoPanel}
                <NewVersionFormPanel
                  on_submit={submitNewVersion}
                  hidden={infoPanel ? true : false}
                >
                  {parse(ingredient.new_version_form)}
                </NewVersionFormPanel>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
