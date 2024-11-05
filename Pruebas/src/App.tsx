import { CredentialResponse, GoogleLogin } from "@react-oauth/google";
import { useEffect, useState } from "react";
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

// interface GoogleCredentialResponse {
//   credential: string;
//   clientId: string;
//   select_by: string;
// }

export default function App() {
  const [state, setState] = useState<Usuario>({
    email: "aaaldana50@gmail.com",
    password: "perropeludo1",
    confirm_password: "perropeludo1",
    nombres: "Angel Arturo",
    apellidos: "Aldana Ayasta",
    id_tipo_usuario: 7,
  });

  useEffect(() => {
    fetch(BASE_URL + "csrf/", {
      credentials: "include",
    })
      .then((res) => res.json())
      .then((data) => console.log(data));
  }, []);

  const handleClick = () => {
    fetch(BASE_URL + "auth/email/", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      credentials: "include",
      body: JSON.stringify(state),
    })
      .then((res) => res.json())
      .then((data) => {
        setState(data);
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
      credentials: "include",
      body: JSON.stringify({
        credential,
        id_tipo_usuario: 7,
      }),
    })
      .then((res) => res.json())
      .then((data) => {
        setState(data);
        console.log(data);
      });
  };

  const handleWhoAmI = () => {
    fetch(BASE_URL + "whoami/", {
      credentials: "include",
    })
      .then((res) => res.json())
      .then((data) => console.log(data));
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
        shape="rectangular"
        theme="filled_blue"
        ux_mode="popup"
        locale="es-PE"
        text="signin"
      ></GoogleLogin>
      <button onClick={handleWhoAmI}>Who Am I</button>
      <pre>{JSON.stringify(state, null, 2)}</pre>
    </div>
  );
}
