import { useEffect, useRef, useState } from "react";

function Publications() {
  const [publications, setPublications] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const loadPublications = async () => {
      try {
        const response = await fetch(
          "http://localhost:5001/api/publications"
        );

        if (!response.ok) {
          throw new Error("Could not load publications");
        }

        const reader = response.body.getReader();
        const decoder = new TextDecoder();

        let buffer = "";

        while (true) {
          const { value, done } = await reader.read();

          if (done) break;

          buffer += decoder.decode(value, {
            stream: true,
          });

          const lines = buffer.split("\n");
          buffer = lines.pop();

          for (const line of lines) {
            if (!line.trim()) continue;

            const publication = JSON.parse(line);

            if (publication.error) {
              throw new Error(publication.error);
            }

            setPublications((previous) => {
              const exists = previous.some(
                (item) => item.pmid === publication.pmid
              );

              if (exists) {
                return previous;
              }

              return [...previous, publication];
            });
          }
        }
      } catch (error) {
        console.error("Error:", error);
        setError(error.message);
      } finally {
        setLoading(false);
      }
    };

    loadPublications();
  }, []);

  return (
    <section className="publications">
      <div className="sectionHeader">
        <h2>Latest Publications</h2>

        {!loading && (
          <span className="count">
            {publications.length} papers
          </span>
        )}
      </div>

      {loading && <p>Loading publications...</p>}

      {error && (
        <p className="error">
          {error}
        </p>
      )}

      <div className="list">
        {publications.map((publication) => (
          <article
            className="card"
            key={publication.pmid}
          >
            <div className="meta">
              <span>{publication.date}</span>
              <span>•</span>
              <span>{publication.journal}</span>
            </div>

            <h3>{publication.title}</h3>

            <Authors authors={publication.authors} />

            {publication.summary && (
              <div className="summaryBox">
                <h4>AI Summary</h4>

                <p className="summary">
                  {publication.summary}
                </p>
              </div>
            )}

            {publication.abstract && (
              <ExpandableAbstract
                abstract={publication.abstract}
              />
            )}

            <div className="footer">
              <span>
                PMID: {publication.pmid}
              </span>

              <a
                href={publication.url}
                target="_blank"
                rel="noreferrer"
              >
                View on PubMed →
              </a>
            </div>
          </article>
        ))}
      </div>
    </section>
  );
}

function Authors({ authors }) {
  const [expanded, setExpanded] = useState(false);
  const [canExpand, setCanExpand] = useState(false);

  const authorsRef = useRef(null);

  const authorsText = Array.isArray(authors)
    ? authors.join(", ")
    : authors;

  useEffect(() => {
    const element = authorsRef.current;

    if (!element) return;

    setCanExpand(
      element.scrollHeight > element.clientHeight
    );
  }, [authorsText]);

  return (
    <div className="expandableSection">
      <p
        ref={authorsRef}
        className={`authors ${
          expanded ? "expanded" : ""
        }`}
      >
        {authorsText}
      </p>

      {canExpand && (
        <button
          className="expandButton"
          onClick={() => setExpanded(!expanded)}
        >
          {expanded
            ? "Show less ▲"
            : "Show all authors ▼"}
        </button>
      )}
    </div>
  );
}

function ExpandableAbstract({ abstract }) {
  const [expanded, setExpanded] = useState(false);
  const [canExpand, setCanExpand] = useState(false);

  const abstractRef = useRef(null);

  useEffect(() => {
    const element = abstractRef.current;

    if (!element) return;

    setCanExpand(
      element.scrollHeight > element.clientHeight
    );
  }, [abstract]);

  return (
    <div className="abstractBox">
      <h4>Abstract</h4>

      <p
        ref={abstractRef}
        className={`abstract ${
          expanded ? "expanded" : ""
        }`}
      >
        {abstract}
      </p>

      {canExpand && (
        <button
          className="expandButton"
          onClick={() => setExpanded(!expanded)}
        >
          {expanded
            ? "Show less ▲"
            : "Read full abstract ▼"}
        </button>
      )}
    </div>
  );
}

export default Publications;