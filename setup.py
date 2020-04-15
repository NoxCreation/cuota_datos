from cx_Freeze import setup, Executable


executables = [
    Executable(
    	script="cuota_datos.py",
    )
]

bdist_msi_options = {
    'add_to_path': True,
    'initial_target_dir': r'[ProgramFilesFolder]\%s\%s' % ("Cuota", "cuota_nauta"),
}

setup(
        name='cuota_datos',
        author='Josué Carballo',
        author_email='josuecb@yandex.com',
        version='0.2',
        description='Para conocer y comprar datos móviles de Etecsa.',
        executables=executables,
        options={
            "bdist_msi": bdist_msi_options,
        },
    )

