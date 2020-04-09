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
        version='0.1',
        description='Devuelve el estado de la cuota de etecsa.',
        executables=executables,
        options={
            "bdist_msi": bdist_msi_options,
        },
    )

