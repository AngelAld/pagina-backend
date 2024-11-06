import { CredentialResponse, GoogleLogin } from "@react-oauth/google";
import { useState } from "react";
import "./App.css";
const BASE_URL = "http://localhost:8000/";
interface Usuario {
  id?: number;
  email: string;
  password: string;
  confirm_password: string;
  nombres: string;
  apellidos: string;
  is_verified?: boolean;
  id_tipo_usuario: number;
  tipo_usuario?: string[];
}

interface Tokens {
  access: string;
  refresh: string;
}

interface PerfilCliente {
  dni: string;
  perfil_cliente: {
    telefono: string;
  };
}

export default function App() {
  const [state, setState] = useState<Usuario>({
    email: "aaaldana50@gmail.com",
    password: "perropeludo1",
    confirm_password: "perropeludo1",
    nombres: "Angel Arturo",
    apellidos: "Aldana Ayasta",
    id_tipo_usuario: 7,
  });
  const [perfil, setPerfil] = useState<PerfilCliente>({
    dni: "71448693",
    perfil_cliente: {
      telefono: "976065217",
    },
  });
  const [data, setData] = useState({});
  const [tokens, setTokens] = useState<Tokens>({
    access: "",
    refresh: "",
  });

  const handleClick = () => {
    fetch(BASE_URL + "auth/email/", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(state),
    })
      .then((res) => res.json())
      .then((data) => {
        setData(data);
        console.log(data);
      });
  };

  const handleGoogleLogin = (credentialResponse: CredentialResponse) => {
    const { credential } = credentialResponse;
    fetch(BASE_URL + "auth/google/", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        credential,
        id_tipo_usuario: 7,
      }),
    })
      .then((res) => res.json())
      .then((data) => {
        setData(data);
        if (data.tokens) {
          setTokens(data.tokens);
        }
      });
  };

  const handleWhoAmI = () => {
    fetch(BASE_URL + "whoami/", {
      headers: {
        Authorization: `Bearer ${tokens.access}`,
      },
    })
      .then((res) => res.json())
      .then((data) => {
        setData(data);
        console.log(data);
        console.log(state);
      })
      .catch((err) => console.log(err));
  };

  const handlePerfil = () => {
    console.log(perfil);
    fetch(BASE_URL + "perfiles/cliente/", {
      method: "POST",
      headers: {
        Authorization: `Bearer ${tokens.access}`,
        "Content-Type": "application/json",
      },
      body: JSON.stringify(perfil),
    })
      .then((res) => res.json())
      .then((data) => {
        setData(data);
        console.log(data);
      });
  };

  return (
    <div className="form-div">
      <input
        type="text"
        placeholder="Email"
        value={state.email}
        onChange={(e) => setState({ ...state, email: e.target.value })}
      />
      <input
        type="password"
        placeholder="Password"
        value={state.password}
        onChange={(e) => setState({ ...state, password: e.target.value })}
      />
      <input
        type="password"
        placeholder="Confirm Password"
        value={state.confirm_password}
        onChange={(e) =>
          setState({ ...state, confirm_password: e.target.value })
        }
      />
      <input
        type="text"
        placeholder="Nombres"
        value={state.nombres}
        onChange={(e) => setState({ ...state, nombres: e.target.value })}
      />
      <input
        type="text"
        placeholder="Apellidos"
        value={state.apellidos}
        onChange={(e) => setState({ ...state, apellidos: e.target.value })}
      />
      <input
        type="number"
        placeholder="ID Tipo Usuario"
        value={state.id_tipo_usuario}
        onChange={(e) =>
          setState({ ...state, id_tipo_usuario: parseInt(e.target.value) })
        }
      />
      <button onClick={handleClick}>Registrar</button>

      <GoogleLogin
        onSuccess={handleGoogleLogin}
        containerProps={{ className: "google-div" }}
        logo_alignment="center"
        itp_support={true}
        size="large"
        shape="square"
        theme="filled_blue"
        ux_mode="popup"
        locale="es-PE"
        text="signin"
      ></GoogleLogin>
      <button onClick={handleWhoAmI}>Who Am I</button>
      <div className="div-pre">
        <pre>{JSON.stringify(data, null, 2)}</pre>
        <pre>{JSON.stringify(tokens, null, 2)}</pre>
      </div>
      <input
        type="text"
        placeholder="dni"
        value={perfil.dni}
        onChange={(e) => setPerfil({ ...perfil, dni: e.target.value })}
      />
      <input
        type="text"
        placeholder="Telefono"
        value={perfil.perfil_cliente.telefono}
        onChange={(e) =>
          setPerfil({
            ...perfil,
            perfil_cliente: {
              ...perfil.perfil_cliente,
              telefono: e.target.value,
            },
          })
        }
      />
      <button onClick={handlePerfil}>Post</button>
    </div>
  );
}
