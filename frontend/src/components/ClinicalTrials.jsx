import { useEffect, useState } from "react";

function ClinicalTrials() {
  const [query, setQuery] = useState("");
  const [trials, setTrials] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const fetchTrials = async (searchQuery) => {
    try {
      setLoading(true);
      setError(null);

      const response = await fetch(
        `http://localhost:5001/api/trials/search?q=${encodeURIComponent(searchQuery)}`
      );

      if (!response.ok) {
        throw new Error("Could not search clinical trials");
      }

      const data = await response.json();

      setTrials(data.slice(0, 10));
    } catch (error) {
      console.error(error);
      setError(error.message);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchTrials("Alzheimer");
  }, []);

  const searchTrials = (event) => {
    event.preventDefault();

    if (!query.trim()) return;

    fetchTrials(query);
  };

  return (
    <section>
      <div className="sectionHeader">
        <div>
          <h2>Clinical Trials</h2>
        </div>

        {!loading && (
          <span className="count">
            {trials.length} trials
          </span>
        )}
      </div>

      <form
        className="trialSearch"
        onSubmit={searchTrials}
      >
        <input
          type="text"
          value={query}
          onChange={(event) =>
            setQuery(event.target.value)
          }
          placeholder="Search Alzheimer's, Parkinson's, FTD..."
        />

        <button type="submit">
          Search
        </button>
      </form>

      {loading && (
        <p>Loading clinical trials...</p>
      )}

      {error && (
        <p className="error">
          {error}
        </p>
      )}

      <div className="list">
        {trials.map((trial) => (
          <article
            className="card"
            key={trial.nct_id}
          >
            <div className="meta">
              <span>{trial.nct_id}</span>
              <span>•</span>
              <span>{trial.status}</span>
            </div>

            <h3>{trial.title}</h3>

            {trial.conditions && (
              <p className="trialConditions">
                {trial.conditions.join(", ")}
              </p>
            )}

            {trial.brief_summary && (
              <p className="abstract">
                {trial.brief_summary}
              </p>
            )}

            <div className="footer">
              <span>{trial.study_type}</span>

              <a
                href={trial.url}
                target="_blank"
                rel="noreferrer"
              >
                View on ClinicalTrials.gov →
              </a>
            </div>
          </article>
        ))}
      </div>
    </section>
  );
}

export default ClinicalTrials;