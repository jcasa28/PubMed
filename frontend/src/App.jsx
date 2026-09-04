import { useState } from "react";
import "./App.css";

import Publications from "./components/Publications";
import News from "./components/News";
import ClinicalTrials from "./components/ClinicalTrials";

function App() {
  const [activeSection, setActiveSection] = useState("publications");

  return (
    <main className="page">

      <section className="hero">
        <p className="eyebrow">
          Institute for Translational Research
        </p>

        <h1>Sid E. O'Bryant</h1>

        <p className="subtitle">
          Research publications, news, and clinical trials.
        </p>
      </section>

    {/* start navigation */}
    <nav className="navbar">

      <button
        onClick={() => setActiveSection("publications")}
        className={activeSection === "publications" ? "navItem active" : "navItem"}
      >
        Publications
      </button>

      <button
        onClick={() => setActiveSection("news")}
        className={activeSection === "news" ? "navItem active" : "navItem"}
      >
        News
      </button>

      <button
        onClick={() => setActiveSection("trials")}
        className={activeSection === "trials" ? "navItem active" : "navItem"}
      >
        Clinical Trials
      </button>
    </nav>
{/* end navigation */}

      {activeSection === "publications" && (
        <Publications />
      )}

      {activeSection === "news" && (
        <News />
      )}

      {activeSection === "trials" && (
        <ClinicalTrials />
      )}

    </main>
  );
}

export default App;