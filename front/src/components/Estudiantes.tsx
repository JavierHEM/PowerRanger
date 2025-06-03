import React, { useEffect, useState } from "react";
import axios from "axios";
import { Paper, Typography, Table, TableBody, TableCell, TableContainer, TableHead, TableRow } from "@mui/material";

const Estudiantes: React.FC = () => {
  const [estudiantes, setEstudiantes] = useState<any[]>([]);

  useEffect(() => {
    const fetchEstudiantes = async () => {
      const token = localStorage.getItem("token");
      const response = await axios.get("http://localhost:8000/api/v1/estudiantes", {
        headers: { Authorization: `Bearer ${token}` }
      });
      setEstudiantes(response.data);
    };
    fetchEstudiantes();
  }, []);

  return (
    <Paper sx={{ p: 3 }}>
      <Typography variant="h5" sx={{ mb: 2, fontWeight: 700 }}>
        Listado de Estudiantes
      </Typography>
      <TableContainer>
        <Table>
          <TableHead>
            <TableRow>
              <TableCell>Nombre</TableCell>
              <TableCell>Email</TableCell>
              {/* Agregar más columnas según el modelo */}
            </TableRow>
          </TableHead>
          <TableBody>
            {estudiantes.map((e) => (
              <TableRow key={e.id}>
                <TableCell>{e.nombre}</TableCell>
                <TableCell>{e.email}</TableCell>
                {/* Agregar más celdas según el modelo */}
              </TableRow>
            ))}
          </TableBody>
        </Table>
      </TableContainer>
    </Paper>
  );
};

export default Estudiantes;