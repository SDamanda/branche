import React from 'react';
import './App.css';

function App() {
  return (
    <div>
      <header>
        <div className="logo">FLUXO</div>
        <nav>
          <a href="#" className="active">Pesquisa de Empresas</a>
          <a href="#">Blog</a>
          <a href="#">Soluções</a>
          <a href="#">Planos</a>
          <a href="#">Contato</a>
          <a href="#">Entrar</a>
          <button className="btn-yellow">Teste Grátis</button>
        </nav>
      </header>
      <section className="main-section">
        <h1>Empresas de todo <span className="highlight">Brasil</span></h1>
        <div className="search-bar">
          <input type="text" placeholder="Busque por CNPJ ou Nome / Cidade" />
          <button>Pesquisar</button>
        </div>
      </section>
    </div>
  );
}

export default App;
