import Footer from "../shared/Footer";

function App() {
  return (
    <>
      <div>
        <h1>Protected Area</h1>
        <p>Welcome to the protected area. You must be logged in to see this.</p>

        <a href="/api/logoutcas">Logout</a>
      </div>
      <Footer />
    </>
  );
}

export default App;
