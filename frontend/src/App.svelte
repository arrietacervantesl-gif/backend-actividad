<script>
  import { onMount } from "svelte";

  const API_URL = "http://127.0.0.1:5000/api/products/products";

  let listdata = [];
  let loading = true;
  let error = "";
  let mensaje = "";

  let search = "";
  let categoryFilter = "todos";
  let showModal = false;
  let editingId = null;
  let saving = false;

  let form = {
    nombre: "",
    descripcion: "",
    precio: "",
    stock_min: 0,
    categoria_id: "",
    disponible: true,
  };

  // Cargar productos desde Flask
  onMount(() => {
    loadProducts();
  });

  async function loadProducts() {
    loading = true;
    error = "";

    try {
      const response = await fetch(API_URL);

      if (!response.ok) {
        throw new Error("No se pudieron consultar los productos.");
      }

      const data = await response.json();

      if (!Array.isArray(data)) {
        throw new Error("La API no devolvió una lista de productos.");
      }

      listdata = data;
    } catch (err) {
      error = err.message;
      console.error(err);
    } finally {
      loading = false;
    }
  }

  // Categorías disponibles según los productos
  $: categories = [
    ...new Map(
      listdata.map((p) => [
        p.categoria_id,
        {
          id: p.categoria_id,
          nombre: p.categoria_nombre || "Categoría " + p.categoria_id,
        },
      ]),
    ).values(),
  ];

  // Buscador y filtros
  $: filteredProducts = listdata.filter((producto) => {
    const texto = (
      (producto.nombre || "") +
      " " +
      (producto.descripcion || "")
    ).toLowerCase();

    const coincideTexto = texto.includes(search.toLowerCase());

    const coincideCategoria =
      categoryFilter === "todos" ||
      String(producto.categoria_id) === categoryFilter;

    return coincideTexto && coincideCategoria;
  });

  $: availableCount = listdata.filter((p) => p.disponible).length;

  function formatPrice(price) {
    return new Intl.NumberFormat("es-CO", {
      style: "currency",
      currency: "COP",
      maximumFractionDigits: 0,
    }).format(Number(price || 0));
  }

  function productIcon(nombre = "") {
    const name = nombre.toLowerCase();

    if (name.includes("camisa") || name.includes("camiseta")) return "👕";
    if (name.includes("zapato") || name.includes("tenis")) return "👟";
    if (name.includes("pantalon")) return "👖";
    if (name.includes("gorra")) return "🧢";
    if (name.includes("celular") || name.includes("telefono")) return "📱";
    if (name.includes("computador")) return "💻";
    if (name.includes("audifono")) return "🎧";
    if (name.includes("reloj")) return "⌚";
    if (name.includes("manzana") || name.includes("fruta")) return "🍎";
    if (name.includes("pan")) return "🥖";
    if (name.includes("leche")) return "🥛";
    if (name.includes("cafe")) return "☕";

    return "📦";
  }

  function openNewProduct() {
    editingId = null;

    form = {
      nombre: "",
      descripcion: "",
      precio: "",
      stock_min: 0,
      categoria_id: "",
      disponible: true,
    };

    error = "";
    mensaje = "";
    showModal = true;
  }

  function openEditProduct(producto) {
    editingId = producto.id;

    form = {
      nombre: producto.nombre || "",
      descripcion: producto.descripcion || "",
      precio: producto.precio ?? "",
      stock_min: producto.stock_min ?? 0,
      categoria_id: producto.categoria_id ?? "",
      disponible: producto.disponible,
    };

    error = "";
    mensaje = "";
    showModal = true;
  }

  async function saveProduct() {
    error = "";
    mensaje = "";

    if (!form.nombre.trim()) {
      error = "Escribe el nombre del producto.";
      return;
    }

    if (!form.precio || Number(form.precio) <= 0) {
      error = "El precio debe ser mayor que cero.";
      return;
    }

    if (!form.categoria_id || Number(form.categoria_id) <= 0) {
      error = "Debes ingresar un ID de categoría válido.";
      return;
    }

    saving = true;

    const productData = {
      nombre: form.nombre.trim(),
      descripcion: form.descripcion.trim(),
      precio: Number(form.precio),
      stock_min: Number(form.stock_min),
      categoria_id: Number(form.categoria_id),
      disponible: form.disponible,
    };

    try {
      const url = editingId ? `${API_URL}/${editingId}` : API_URL;

      const response = await fetch(url, {
        method: editingId ? "PUT" : "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(productData),
      });

      const result = await response.json();

      if (!response.ok) {
        throw new Error(
          result.description ||
            result.mensaje ||
            result.message ||
            "No se pudo guardar el producto.",
        );
      }

      showModal = false;
      mensaje = editingId
        ? "Producto actualizado correctamente."
        : "Producto registrado correctamente.";

      await loadProducts();
    } catch (err) {
      error = err.message;
    } finally {
      saving = false;
    }
  }

  async function deleteProduct(id) {
    const confirmar = confirm(
      "¿Estás seguro de que deseas eliminar este producto?",
    );

    if (!confirmar) return;

    error = "";
    mensaje = "";

    try {
      const response = await fetch(`${API_URL}/${id}`, {
        method: "DELETE",
      });

      const result = await response.json();

      if (!response.ok) {
        throw new Error(
          result.description ||
            result.mensaje ||
            "No se pudo eliminar el producto.",
        );
      }

      mensaje = "Producto eliminado correctamente.";
      await loadProducts();
    } catch (err) {
      error = err.message;
    }
  }
</script>

<svelte:head>
  <title>ActORM | Tienda de productos</title>
  <meta
    name="description"
    content="Catálogo y administración de productos ActORM"
  />
</svelte:head>

<div class="app">
  <!-- BARRA SUPERIOR -->
  <header class="topbar">
    <div class="brand">
      <div class="brand-icon">A</div>
      <div>
        <h2>ActORM</h2>
        <span>TIENDA VIRTUAL</span>
      </div>
    </div>

    <div class="topbar-right">
      <span class="connection">
        <span class="connection-dot"></span>
        Catálogo de productos
      </span>

      <button class="add-button" onclick={openNewProduct}>
        <span>＋</span> Nuevo producto
      </button>
    </div>
  </header>

  <main class="main-content">
    <!-- PRESENTACIÓN -->
    <section class="welcome">
      <div>
        <span class="eyebrow">PANEL DE ADMINISTRACIÓN</span>
        <h1>Tu catálogo de productos</h1>
        <p>
          Administra, consulta y organiza todos tus productos desde un solo
          lugar.
        </p>
      </div>

      <div class="welcome-decoration">🛍️</div>
    </section>

    <!-- ESTADÍSTICAS -->
    <section class="stats">
      <div class="stat-card">
        <div class="stat-icon purple">📦</div>
        <div>
          <span>Total de productos</span>
          <strong>{listdata.length}</strong>
        </div>
      </div>

      <div class="stat-card">
        <div class="stat-icon green">✓</div>
        <div>
          <span>Disponibles</span>
          <strong>{availableCount}</strong>
        </div>
      </div>

      <div class="stat-card">
        <div class="stat-icon orange">▤</div>
        <div>
          <span>Categorías</span>
          <strong>{categories.length}</strong>
        </div>
      </div>
    </section>

    <!-- CATÁLOGO -->
    <section class="catalog">
      <div class="catalog-heading">
        <div>
          <h2>Productos</h2>
          <p>Consulta y administra tu inventario.</p>
        </div>

        <button class="refresh-button" onclick={loadProducts}>
          ↻ Actualizar
        </button>
      </div>

      <!-- BUSCADOR Y FILTROS -->
      <div class="filters">
        <div class="search-box">
          <span>⌕</span>
          <input
            type="search"
            placeholder="Buscar productos por nombre..."
            bind:value={search}
          />
        </div>

        <select bind:value={categoryFilter}>
          <option value="todos">Todas las categorías</option>

          {#each categories as category}
            <option value={String(category.id)}>
              {category.nombre}
            </option>
          {/each}
        </select>
      </div>

      {#if mensaje}
        <div class="success-message">{mensaje}</div>
      {/if}

      {#if error && !showModal}
        <div class="error-message">{error}</div>
      {/if}

      {#if loading}
        <div class="empty-state">
          <div class="loading-spinner"></div>
          <h3>Cargando productos...</h3>
          <p>Estamos consultando tu base de datos.</p>
        </div>
      {:else if filteredProducts.length > 0}
        <div class="product-grid">
          {#each filteredProducts as producto (producto.id)}
            <article class="product-card">
              <div class="product-image">
                <span class="product-emoji">
                  {productIcon(producto.nombre)}
                </span>

                <span
                  class:unavailable={!producto.disponible}
                  class="availability"
                >
                  {producto.disponible ? "Disponible" : "No disponible"}
                </span>
              </div>

              <div class="product-info">
                <span class="category-label">
                  {producto.categoria_nombre ||
                    "Categoría " + producto.categoria_id}
                </span>

                <h3>{producto.nombre}</h3>

                <p class="description">
                  {producto.descripcion || "Sin descripción disponible."}
                </p>

                <div class="price">
                  {formatPrice(producto.precio)}
                </div>

                <div class="stock">
                  Stock mínimo: {producto.stock_min ?? 0}
                </div>

                <div class="card-actions">
                  <button
                    class="edit-button"
                    onclick={() => openEditProduct(producto)}
                  >
                    ✎ Editar
                  </button>

                  <button
                    class="delete-button"
                    onclick={() => deleteProduct(producto.id)}
                    aria-label="Eliminar producto"
                  >
                    🗑
                  </button>
                </div>
              </div>
            </article>
          {/each}
        </div>
      {:else}
        <div class="empty-state">
          <div class="empty-icon">📦</div>

          {#if search || categoryFilter !== "todos"}
            <h3>No encontramos productos</h3>
            <p>Prueba con otra búsqueda o categoría.</p>
          {:else}
            <h3>Tu catálogo está vacío</h3>
            <p>Todavía no tienes productos registrados en tu base de datos.</p>
            <button class="add-button" onclick={openNewProduct}>
              ＋ Registrar primer producto
            </button>
          {/if}
        </div>
      {/if}

      <div class="results-footer">
        Mostrando {filteredProducts.length} de {listdata.length} productos
      </div>
    </section>
  </main>

  <footer class="footer">
    <strong>ActORM</strong> · Sistema de administración de productos
  </footer>
</div>

<!-- VENTANA PARA REGISTRAR Y EDITAR -->
{#if showModal}
  <div class="modal-overlay">
    <section class="modal">
      <div class="modal-header">
        <div>
          <span class="eyebrow">GESTIÓN DE INVENTARIO</span>
          <h2>{editingId ? "Editar producto" : "Nuevo producto"}</h2>
        </div>

        <button class="close-button" onclick={() => (showModal = false)}>
          ×
        </button>
      </div>

      <form
        onsubmit={(event) => {
          event.preventDefault();
          saveProduct();
        }}
      >
        <label>
          Nombre del producto *
          <input
            type="text"
            bind:value={form.nombre}
            placeholder="Ej. Camiseta deportiva"
            required
          />
        </label>

        <label>
          Descripción
          <textarea
            bind:value={form.descripcion}
            placeholder="Describe las características del producto..."
            rows="3"></textarea>
        </label>

        <div class="form-row">
          <label>
            Precio *
            <input
              type="number"
              min="0.01"
              step="0.01"
              bind:value={form.precio}
              placeholder="35000"
              required
            />
          </label>

          <label>
            Stock mínimo *
            <input
              type="number"
              min="0"
              step="1"
              bind:value={form.stock_min}
              required
            />
          </label>
        </div>

        <label>
          ID de categoría *
          <input
            type="number"
            min="1"
            step="1"
            bind:value={form.categoria_id}
            placeholder="Ej. 1"
            required
          />
          <small>Debes utilizar un ID que exista en tu tabla categorias.</small>
        </label>

        <label class="availability-check">
          <input type="checkbox" bind:checked={form.disponible} />
          Producto disponible
        </label>

        {#if error && showModal}
          <div class="error-message">{error}</div>
        {/if}

        <div class="modal-actions">
          <button
            type="button"
            class="cancel-button"
            onclick={() => (showModal = false)}
          >
            Cancelar
          </button>

          <button type="submit" class="add-button" disabled={saving}>
            {saving
              ? "Guardando..."
              : editingId
                ? "Guardar cambios"
                : "Registrar producto"}
          </button>
        </div>
      </form>
    </section>
  </div>
{/if}
